import datetime
from enum import IntEnum
import json
from typing import Iterable

from .connection import get_connection
from .model import NotificationPattern


class InvokationType(IntEnum):
    BY_EVENT = 1
    BY_TIME = 2
    MANUAL = 3


class DBHelper:
    def __init__(self, get_connection_):
        self.get_connection = get_connection_

    def choose_event_pattern(self, event_type: str) -> NotificationPattern:
        with self.get_connection() as connection:
            with connection.cursor() as cur:
                sql = (
                    "SELECT id, pattern_file, actual_time, settings_"
                    " FROM notification_pattern"
                    " WHERE type_=%s AND CAST(settings_::json->'event_type' AS VARCHAR) = %s"
                )
                cur.execute(sql, (InvokationType.BY_EVENT.value, f'"{event_type}"'))
                row = cur.fetchone()
                if not row:
                    raise ValueError(f"No event pattern for event {event_type}")
                return NotificationPattern(**row)

    def add_notification_event(self, message_id: str, pattern_id: int):
        with self.get_connection() as connection:
            with connection.cursor() as cur:
                sql = "INSERT INTO notification_event (pattern, source, start_time)" " VALUES (%s, %s, %s)"
                data = (pattern_id, json.dumps({"message_id": message_id}), datetime.datetime.now())
                cur.execute(sql, data)
                connection.commit()

    def get_time_patterns(self) -> Iterable[NotificationPattern]:
        sql = "SELECT * FROM notification_pattern WHERE type_=%s"
        with self.get_connection() as connection:
            with connection.cursor() as cur:
                cur.execute(sql, (InvokationType.BY_TIME.value,))
                result = cur.fetchall()
                return [NotificationPattern(**item) for item in result]

    def already_was_msg_id(self, message_id: str) -> bool:
        sql = "SELECT COUNT(*) FROM notification_event WHERE source::jsonb->>'message_id' = %s"
        with self.get_connection() as connection:
            with connection.cursor() as cur:
                cur.execute(sql, (message_id,))
                row = cur.fetchone()
                print(row)
                count = int(row["count"])
                return count > 0


db_helper = DBHelper(get_connection)
