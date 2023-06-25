FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint script as the entrypoint of the container
ENTRYPOINT ["/app/entrypoint.sh"]
