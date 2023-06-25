FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

# Копирование файлов
COPY run_uwsgi.sh run_uwsgi.sh
COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

# Установка зависимостей
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов
COPY app.py app.py
COPY src src

# Добавление разрешений для выполнения скрипта
RUN chmod +x run_uwsgi.sh

# Измененная команда для запуска с использованием скрипта
ENTRYPOINT ["./run_uwsgi.sh"]
