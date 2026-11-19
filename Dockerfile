FROM python:3.12.7-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy dependency definitions first to improve build-cache reuse.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && groupadd --system appgroup \
    && useradd --system --uid 10001 --gid appgroup appuser

COPY --chown=appuser:appgroup app.py .

USER 10001:appgroup

# Flask/Gunicorn listens on TCP port 5000.
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
