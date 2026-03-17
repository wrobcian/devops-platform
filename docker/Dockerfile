FROM python:3.11-slim

LABEL maintainer="devops-learner"
LABEL description="DevOps Platform Application"
LABEL version="1.0.0"

ENV ENVIRONMENT=production \
    APP_VERSION=1.0.0 \
    PORT=5000 \
    LOG_LEVEL=INFO \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/main.py .

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

CMD ["python", "main.py"]