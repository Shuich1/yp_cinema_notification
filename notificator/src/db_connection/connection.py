from contextlib import contextmanager
import psycopg
from psycopg.rows import dict_row

from src.config import settings


@contextmanager
def get_connection():
    connection = psycopg.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        user=settings.postgres_user,
        password=settings.postgres_password,
        dbname=settings.postgres_db_name,
        row_factory=dict_row,
    )
    yield connection
    connection.close()
