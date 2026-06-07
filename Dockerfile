FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8998

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8998", "app:app", "--access-logfile=-"]
