FROM python:3.10-slim

COPY requirements.txt /
RUN pip install -U pip && pip install -r requirements.txt

COPY app/ /app
EXPOSE 8000

CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload