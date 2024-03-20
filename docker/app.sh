#!/bin/bash

alembic upgrade head

gunicorn -w 4 -k uvicorn.workers.UvicornWorker lonely_eye.main:app --bind 0.0.0.0:8000