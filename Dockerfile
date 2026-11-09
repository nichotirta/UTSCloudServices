# builder
FROM python:3.12.7-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# runtime
FROM python:3.12.7-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY --from=builder /install /usr/local
COPY app.py .
COPY templates ./templates
EXPOSE 5000
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]