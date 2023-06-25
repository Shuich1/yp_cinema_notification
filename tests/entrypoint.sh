#!/bin/bash

# Function to check if PostgreSQL is up
wait_for_postgres() {
    echo "Waiting for PostgreSQL to start"

    host="$1"
    port="$2"
    retries=5
    while [[ $retries -ge 0 ]]
    do
        nc -z "$host" "$port"
        result=$?

        if [ $result -eq 0 ]; then
            echo "PostgreSQL started"
            return 0
        fi

        retries=$((retries-1))
        sleep 10
    done

    echo "Failed to connect to PostgreSQL"
    return 1
}

# Function to check if RabbitMQ is up
wait_for_rabbitmq() {
    echo "Waiting for RabbitMQ to start"

    host="$1"
    port="$2"
    retries=5
    while [[ $retries -ge 0 ]]
    do
        nc -z "$host" "$port"
        result=$?

        if [ $result -eq 0 ]; then
            echo "RabbitMQ started"
            return 0
        fi

        retries=$((retries-1))
        sleep 10
    done

    echo "Failed to connect to RabbitMQ"
    return 1
}

# Call the function with PostgreSQL host and port
wait_for_postgres "notificator_postgres" 5432

# Call the function with RabbitMQ host and port
wait_for_rabbitmq "rabbitmq" 5672

# Execute your Python script
python -m unittest test_notification.py
