# 多阶段构建
FROM python:3.11-slim AS builder
WORKDIR /app
COPY pyproject.toml setup.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim AS runtime
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY longcache/ ./longcache/
COPY config.example.json ./config.example.json
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["python", "-m", "longcache", "serve"]
