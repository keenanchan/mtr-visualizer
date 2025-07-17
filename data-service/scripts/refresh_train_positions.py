"""
refresh_train_positions.py
    - Rerun and refresh the current_train_positions materialized view

usage:
    python refresh_train_positions.py
"""

import os
import sys
import psycopg2
import pika

from pika.exchange_type import ExchangeType

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "timescaledb"),
    port=os.getenv("DB_PORT", 5432),
    dbname=os.getenv("POSTGRES_DB", "mtr"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres")
)

cur = conn.cursor()

def callback(channel, method, properties, body):
    try:
        with open("/scripts/compute_current_positions.sql", "r") as f:
            query = f.read()
        cur.execute(query)
        conn.commit()

        print("Refreshed train positions.")

    except Exception as e:
        print(f"Error refreshing: {e}")
        conn.rollback()
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    else:
        channel.basic_ack(delivery_tag=method.delivery_tag)

def main():
    # RabbitMQ connection setup
    # Create a blocking connection to the queue.
    mq_params = pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST"))
    mq_connection = pika.BlockingConnection(mq_params)
    mq_channel = mq_connection.channel()

    # Declare an exchange.
    # We want this to be direct
    mq_channel.exchange_declare(
        exchange='mtr',
        exchange_type=ExchangeType.topic.value
    )

    # Declare another queue - this one notifies data-service when ingestion is done
    # This is to trigger materialized view updates
    mq_channel.queue_declare(queue="ingest.done", durable=True)

    mq_channel.queue_bind(
        exchange='mtr',
        queue='ingest.done',
        routing_key='ingest.done'
    )

    # Define consume behaviour
    mq_channel.basic_consume(
        queue="ingest.done",
        on_message_callback=callback
    )

    mq_channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
