FROM python:3.13-slim-bookworm

COPY requirements.txt requirements.txt
RUN pip install --compile --no-cache-dir -r requirements.txt

COPY app app
COPY main.py main.py

RUN python -m compileall app main.py

ENV PORT="8080"
ENV WORKERS="1"

ENTRYPOINT gunicorn main:app --workers=${WORKERS} --worker-class=uvicorn.workers.UvicornWorker --bind=0.0.0.0:${PORT}
