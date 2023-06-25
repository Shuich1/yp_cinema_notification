import logging
from logging import getLogger

from flask import current_app

from src.common_send import send_all
from src.db_connection.helper import db_helper


logger = getLogger()
logging.basicConfig(level=logging.INFO)


def on_time():
    current_app.logger.info("Invoked on time")
    users = ["forintricework@gmail.com", "forintricework95@gmail.com"]
    patterns = db_helper.get_time_patterns()
    send_all(users, patterns)
