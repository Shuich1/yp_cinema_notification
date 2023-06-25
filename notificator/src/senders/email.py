import os
from email.message import EmailMessage
from http import HTTPStatus
from typing import List, Tuple

from flask import current_app
from jinja2 import Environment, FileSystemLoader

from src.config import settings
from src.utils.smtp_connect import connect_smtp_sever


class EmailSender:
    def __init__(self):
        self.smtp_server = connect_smtp_sever(
            settings.smtp_server, settings.smtp_server_port, settings.email_user, settings.email_password
        )
        path = f"{os.path.dirname(__file__)}/html_template"
        self.template_env = Environment(loader=FileSystemLoader(path))

    def send_mail(
        self, destination: List[str], subject: str, html_template: str, title: str, text: str, image: str = ""
    ) -> Tuple[str, HTTPStatus]:
        message = self.create_message(destination, subject, html_template, title, text, image)
        try:
            self.smtp_server.sendmail(settings.email_user, destination, message.as_string())
        except Exception as e:
            current_app.logger.error(e)
        return "Success", HTTPStatus.OK

    def create_message(
        self, destination: List[str], subject: str, html_template: str, title: str, text: str, image: str
    ) -> EmailMessage:
        message = EmailMessage()
        message["From"] = settings.email_user
        message["To"] = destination
        message["Subject"] = subject

        template = self.template_env.get_template(html_template)
        output = template.render(title=title, text=text, image=image)
        message.add_alternative(output, subtype="html")

        return message
