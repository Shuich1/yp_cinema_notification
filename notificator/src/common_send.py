import logging
from typing import Iterable

from src.db_connection.helper import db_helper
from src.senders.email import EmailSender
from flask import current_app
from src.db_connection.model import User
from src.db_connection.model import NotificationPattern

logger = logging.getLogger()


def send_email(user: User, pattern: NotificationPattern):
    addresses = [user["email"]]
    file_pattern = pattern.pattern_file
    settings_ = pattern.settings_

    # Create an instance of the EmailSender class
    email_sender = EmailSender()

    # Use this instance to call the send_mail method
    email_sender.send_mail(
        addresses, settings_["subject"], file_pattern, settings_["title"], settings_["text"], settings_["image"]
    )

    current_app.logger.info(f"Sent to {addresses}, {file_pattern}, {settings_}")


def send_all(users: Iterable[User], patterns: Iterable[NotificationPattern], message_id=None):
    """Send to all channels - email, telegram and so on.
    message_id actual only for event from RabbitMQ.
    """
    if message_id is not None:
        if db_helper.already_was_msg_id(message_id):
            logger.warning("Message id %s already sent, exiting.", message_id)
            return
    for pattern in patterns:
        for user in users:
            print(user, pattern)
            send_email(user, pattern)
        db_helper.add_notification_event(message_id, pattern.id)
