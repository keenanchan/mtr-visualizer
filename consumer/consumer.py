import pika
import sys
import os
import logging
import json
import psycopg2
import pytz

from datetime import datetime
from pika.exchange_type import ExchangeType
from psycopg2.extras import execute_values

logging.basicConfig(level=logging.INFO)

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "timescaledb"),
    port=os.getenv("DB_PORT", 5432),
    dbname=os.getenv("DB_NAME", "mtr"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "postgres"),
)

# SQL to insert into train_eta_raw table
INSERT_SQL = """
INSERT INTO train_eta_raw
(line_code, station_code, destination, platform, direction, eta)
VALUES %s
"""


# Helper fn turning API JSON to list-of-tuples
def unpack_eta_snapshot(payloads):
    
    rows = []
    
    # timezone internal processing
    hk_tz = pytz.timezone("Asia/Hong_Kong")
    utc = pytz.UTC

    for payload in payloads:
        if payload.get("status", 0) == 0 or payload.get("sys_time", "-") == "-":
            continue
        for line_station, station_data in payload.get("data", {}).items():
            line_code, station_code = line_station.split('-')
            for direction in ("UP", "DOWN"):
                for eta in station_data.get(direction, []):

                    eta_utc = hk_tz.localize(
                        datetime.strptime(
                            eta["time"],
                            "%Y-%m-%d %H:%M:%S"
                        )
                    ).astimezone(utc)

                    rows.append((
                        line_code,      # line_code     TEXT
                        station_code,   # station_code  TEXT
                        eta['dest'],    # destination   TEXT
                        eta['plat'],    # platform      TEXT
                        direction,      # direction     TEXT
                        eta_utc,    # eta           TIMESTAMPTZ (ISO-8601)
                    ))
    return rows


# Callback fn to be called on message received
def callback(channel, method, properties, body):
    
    try:
        payloads = json.loads(body)
        print(payloads)
        rows = unpack_eta_snapshot(payloads)
        # print(rows[0])
        if not rows:    # just ack if nothing to save
            channel.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        with conn, conn.cursor() as cur:    # commit on success
            execute_values(cur, INSERT_SQL, rows, page_size=100)

        channel.basic_publish(
            exchange='mtr',
            routing_key='ingest.done',
            body=json.dumps({'status': 'success'})
        )

        channel.basic_ack(delivery_tag=method.delivery_tag)
        logging.info("Inserted %d ETA rows", len(rows))
    
    except Exception as e:  # catch everything to NACK safely
        logging.exception("Failed to process message: %s", e)

        # requeue=False so we don't loop poison msgs forever
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


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

    # Declare a queue on the channel. Msgs sent to a non-existent queue will just get dropped!
    mq_channel.queue_declare(queue="mtr_eta", durable=True)

    # Declare another queue - this one notifies data-service when ingestion is done
    # This is to trigger materialized view updates
    mq_channel.queue_declare(queue="ingest.done", durable=True)

    # Bind the queue names to the exchange.
    mq_channel.queue_bind(
        exchange='mtr',
        queue="mtr_eta",
        routing_key="eta"
    )

    mq_channel.queue_bind(
        exchange='mtr',
        queue='ingest.done',
        routing_key='ingest.done'
    )

    # Define consume behaviour
    mq_channel.basic_consume(
        queue="mtr_eta",
        on_message_callback=callback
    )

    # Announce waiting for messages
    logging.info(' [*] Waiting for messages...')
    mq_channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)