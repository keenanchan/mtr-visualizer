import pika
import requests
import json
import time
import sys, os
import logging

from pika.exchange_type import ExchangeType
from line_station import Line, line_stations

# logging basic config
logging.basicConfig(level=logging.INFO)

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

# Hardcoded routing_key for now!
LINES = [Line.ISL, Line.TWL, Line.KTL]

def main():

    logging.info(" [*] Started producer loop.")

    while True:
        # Create message
        try:
            payload = []
            for line in LINES:
                for station in line_stations[line]:
                    response = requests.get(f"https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php?line={line.value}&sta={station.value}")
                    data = response.json()
                    payload.append(data)
                    
                    
                    # mq_channel.basic_publish(
                    #     exchange='mtr',
                    #     routing_key="eta",
                    #     body=message
                    # )

                    time.sleep(0.1)

            message = json.dumps(payload)
            mq_channel.basic_publish(
                exchange='mtr',
                routing_key='eta',
                body=message
            )

            logging.info(f" [x] Sent API payload to queue")
            time.sleep(10) # Poll every minute

        except Exception as e:
            logging.error("Error fetching or sending:", e)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Interrupted")

        # Close out connection
        mq_connection.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)