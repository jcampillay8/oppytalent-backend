FROM python:3.12-slim

WORKDIR /app

# Instalar 'uv' directamente desde su imagen oficial (súper rápido)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY requirements.txt .
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Instalar dependencias en segundos usando uv
RUN uv pip install --system --no-cache -r requirements.txt

COPY . .

EXPOSE 8000

CMD sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"
