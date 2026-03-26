# Dockerfile for Workstation v0.9 Ultimate Flagship
# 1. Backend Service
FROM python:3.12-slim as backend

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

COPY . .

EXPOSE 8000

CMD ["python", "agentic_core/main.py"]

# 2. Frontend Service
FROM node:20-slim as frontend

WORKDIR /app

COPY apps/web/package.json apps/web/package-lock.json ./
RUN npm install

COPY apps/web .
COPY packages ../packages

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
