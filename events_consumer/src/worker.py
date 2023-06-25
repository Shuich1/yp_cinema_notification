import json
import logging
import os

import pika
import requests


# Use a function to setup logger to avoid polluting the global namespace.
def setup_logger():
    logger = logging.getLogger()
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)
    return logger


class Worker:
    def __init__(self, logger):
        self.logger = logger
        self.setup_worker()

    def setup_worker(self):
        host = os.getenv("NOTIFICATOR_HOST")
        port = os.getenv("NOTIFICATOR_PORT")
        event_url = os.getenv("ON_EVENT_URL")
        self.url = f"http://{host}:{port}{event_url}"

    def callback(self, ch, method, properties, body):
        try:
            self.logger.info(body)
            result = self.post_event(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            self.logger.info(result.text)
        except requests.exceptions.RequestException as e:
            self.logger.error(str(e))

    def post_event(self, body):
        return requests.post(self.url, json=json.loads(body), headers={"Content-Type": "application/json"})

    def main(self):
        broker_host = os.getenv("BROKER_HOST")
        self.logger.info("Connecting to %s", broker_host)
        queue_name = os.getenv("QUEUE_NAME")
        connection = self.connect_to_broker(broker_host)
        self.consume_messages(queue_name, connection)

    def connect_to_broker(self, broker_host):
        return pika.BlockingConnection(pika.ConnectionParameters(broker_host))

    def consume_messages(self, queue_name, connection):
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=False)
        channel.basic_qos(prefetch_count=1)
        channel.start_consuming()


if __name__ == "__main__":
    logger = setup_logger()
    worker = Worker(logger)
    worker.main()
