#!/bin/sh
alembic upgrade head &&
uvicorn app.main:app --reload --host ${HOST} --port ${PORT} --proxy-headers
