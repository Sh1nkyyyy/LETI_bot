FROM python:3.13-slim

ENV TZ=Europe/Moscow
ENV PYTHONUNBUFFERED=1

WORKDIR /app


COPY requirements.txt .
RUN pip install --no--cached-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]