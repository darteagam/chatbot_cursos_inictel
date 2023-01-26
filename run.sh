#!bin/bash
source venv/bin/activate
gunicorn main:app -k uvicorn.workers.UvicornWorker -D