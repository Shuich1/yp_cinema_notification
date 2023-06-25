import json
import os
import time
from unittest import IsolatedAsyncioTestCase
from uuid import uuid4

from aio_pika import connect_robust, Message, DeliveryMode
import psycopg
from psycopg.rows import dict_row


class TestMain(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        """
        Setup function to establish the database connection.
        """
        self.connection = psycopg.connect(
            host=os.environ.get("NOTIFICATION_PG_HOST", "0.0.0.0"),
            port=os.environ.get("NOTIFICATION_PG_PORT", "5432"),
            user=os.environ.get("NOTIFICATION_PG_USER", "app"),
            password=os.environ.get("NOTIFICATION_PG_PASSWORD", "123qwe"),
            dbname=os.environ.get("NOTIFICATION_DB_NAME", "notification"),
            row_factory=dict_row,
        )

    async def init_rabbitmq_connection(self):
        broker_host = os.environ.get("BROKER_HOST", "0.0.0.0")
        conn_sting = f"amqp://guest:guest@{broker_host}/"
        connection = await connect_robust(conn_sting)
        return connection

    async def send_to_rmq(self):
        queue_name = os.environ.get("QUEUE_NAME", "ugc_events")
        connection = await self.init_rabbitmq_connection()
        async with connection:
            channel = await connection.channel()

            await channel.declare_queue(name=queue_name, durable=True)
            user_id = str(uuid4())
            payload = {
                "event_type": "review_like",
                "author_id": user_id,
                "review": "4210cb994ae39a084ff36",
                "user_email": "forintricework@gmail.com",
            }
            message_id = str(uuid4())
            message = json.dumps({"message_id": message_id, "payload": payload})
            await channel.default_exchange.publish(
                Message(body=message.encode(), delivery_mode=DeliveryMode.PERSISTENT),
                routing_key=queue_name,
            )
            await connection.close()
            return message_id

    async def test_main(self):
        """
        Main testing function to send message to RabbitMQ and
        check if it's inserted into the database.
        """
        message_id = await self.send_to_rmq()
        time.sleep(10)  # wait for 10 seconds to process everything

        # We take the row for last 100 entries and find our one:
        inserted_row = self.find_in_last_entries(100, message_id)
        self.assertIsNotNone(inserted_row)

    def find_in_last_entries(self, count, message_id):
        """
        Function to find a specific message in the last 'count' entries in the database.
        Args:
            count (int): Number of last entries to consider.
            message_id (str): The message ID to match.
        Returns:
            tuple: The first row from the result of the SQL query.
                   Returns None if no matching record is found.
        """
        cur = self.connection.cursor()

        # Define the SQL query
        sql = (
            f"SELECT * FROM notification_event "
            f"WHERE source::jsonb->>'message_id' = '{message_id}' "
            f"ORDER BY start_time DESC LIMIT {count}"
        )

        # Execute the SQL statement
        cur.execute(sql)

        # Fetch the first row from the results
        row = cur.fetchone()

        # Return the row
        return row
