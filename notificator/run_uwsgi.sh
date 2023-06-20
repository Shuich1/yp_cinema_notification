#!/usr/bin/env bash

set -e

uwsgi --strict --ini uwsgi.ini
