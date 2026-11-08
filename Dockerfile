FROM python:3.13-slim

ENV TZ=Europe/Moscow
ENV PYTHONUNBUFFERED=1

WORKDIR /bot


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot ./bot

CMD ["python", "bot/main.py"]
