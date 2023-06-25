import logging
from logging.config import dictConfig

from pydantic import BaseSettings, Field

from src.utils.smtp_connect import connect_smtp_sever


class Settings(BaseSettings):
    host: str = Field("0.0.0.0", env="NOTIFICATOR_HOST")
    port: int = Field(5000, env="NOTIFICATOR_PORT")
    email_user: str = Field("yp2023cohort23@yandex.ru", env="EMAIL_USER")
    email_password: str = Field("test", env="EMAIL_PASSWORD")
    postgres_host: str = Field("notificator_postgres", env="NOTIFICATION_PG_HOST")
    postgres_port: int = Field(5432, env="NOTIFICATION_PG_PORT")
    postgres_user: str = Field("app", env="NOTIFICATION_PG_USER")
    postgres_password: str = Field("123qwe", env="NOTIFICATION_PG_PASSWORD")
    postgres_db_name: str = Field("notification", env="NOTIFICATION_DB_NAME")
    smtp_server: str = Field("smtp.yandex.ru", env="SMTP_SERVER")
    smtp_server_port: int = Field(465, env="SMTP_SERVER_PORT")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"

    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {"wsgi": {"class": "logging.StreamHandler", "formatter": "default"}},
            "root": {"level": "INFO", "handlers": ["wsgi"]},
        }
    )


settings = Settings()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
