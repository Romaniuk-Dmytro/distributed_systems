#!/bin/bash

uvicorn logging_main:app --reload --port 8082 &
uvicorn logging_main:app --reload --port 8083 &
uvicorn logging_main:app --reload --port 8084 &

