#!/bin/sh

set -e

docker-compose up -d --build --renew-anon-volumes
docker logs -f notification-tests
exitcode="$(docker inspect notification-tests --format={{.State.ExitCode}})"
docker-compose down --remove-orphans --volumes
exit "$exitcode"
