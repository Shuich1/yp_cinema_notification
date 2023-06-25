from flask_restful import reqparse

manual_sender_parser = reqparse.RequestParser()
manual_sender_parser.add_argument("destination", help="Mailing list", required=True)
manual_sender_parser.add_argument("subject", required=True)
manual_sender_parser.add_argument("html_template", help="html template name", required=True)
manual_sender_parser.add_argument("title", required=True)
manual_sender_parser.add_argument("text", required=True)
manual_sender_parser.add_argument("image", required=False)
