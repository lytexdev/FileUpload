FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV FLASK_ENV=production

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
