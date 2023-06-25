import smtplib


def connect_smtp_sever(server: str, port: int, user: str, password: str) -> smtplib.SMTP_SSL:
    mail_server = smtplib.SMTP_SSL(server, port)
    print(user)
    mail_server.login(user, password)
    return mail_server
