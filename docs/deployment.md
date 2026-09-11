# 部署

## Docker

```bash
docker build -t longcache .
docker run -p 8000:8000 longcache
```

## Docker Compose

```bash
docker compose up -d
```

## Kubernetes

```bash
kubectl apply -f deploy/k8s/
```

含 Deployment / Service / HPA / ConfigMap 四件套。
