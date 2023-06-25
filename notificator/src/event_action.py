from flask import Blueprint, request, current_app

from .common_send import send_all
from .resources.parsers.event_action import manual_sender_parser
from .senders.email import EmailSender
from .db_connection.helper import db_helper
from .db_connection.model import User


V1 = "/v1"
event_page = Blueprint("event_page", __name__, url_prefix=V1)
manual = Blueprint("manual", __name__, url_prefix=V1)


@event_page.route("/on_event", methods=["POST"])
def on_event():
    payload = request.json["payload"]
    notification_event_pattern = db_helper.choose_event_pattern(payload["event_type"])
    user_uuid = payload["author_id"]
    users = [User(email=payload["user_email"])]
    message_id = request.json["message_id"]
    send_all(users, [notification_event_pattern], message_id)
    current_app.logger.info("route works, data: %s", request.data)
    return f"route works, data: {request.data}"


@manual.route("/manual_sender", methods=["POST"])
def manual_sender():
    data = manual_sender_parser.parse_args()
    payload, status = EmailSender.send_mail(
        data["destination"], data["subject"], data["html_template"], data["title"], data["text"], data["image"]
    )
    current_app.logger.info("Successful")
    return payload, status
