FROM python:3.11-slim as builder
WORKDIR /app
RUN apt-get update && apt-get install -y gcc g++ git curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
# Removed: apt-get install sqlite3
COPY --from=builder /usr/local /usr/local
COPY . .
# Removed: python data/init_db.py  (Alembic handles it)
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]