# ShopOps — DevOps practice project

A small Flask `shop-api` used to practise containerisation, CI, Kubernetes deployment,
log analysis and incident troubleshooting. This is a learning/demo project, not a
production commerce system.

## Architecture

- Flask + Gunicorn API on TCP port 5000
- Docker image runs as non-root UID 10001
- Docker Compose for local container execution
- GitHub Actions: pytest, Docker build tagged by commit SHA, Trivy image scan
- Kubernetes Deployment (3 replicas) and internal ClusterIP Service
- Python script to count nginx client IPs returning HTTP 5xx responses

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
gunicorn -b 0.0.0.0:5000 app:app
```

In another terminal:

```bash
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:5000/inventory
curl -X POST http://127.0.0.1:5000/orders \
  -H 'Content-Type: application/json' \
  -d '{"product":"keyboard","quantity":2}'
```

## Run with Docker

```bash
docker build -t shop-api:local .
docker run --rm -p 5000:5000 shop-api:local
```

Or:

```bash
docker compose up --build
docker compose down
```

## Log analysis

```bash
python scripts/analyze_logs.py sample-access.log
```

## Kubernetes

The manifest uses the example image `registry.example.com/shop-api:1.4.2` from the
assessment prompt. Replace it with an image you have actually built and pushed to a
registry before deploying.

```bash
kubectl apply -f k8s/shop-api.yaml
kubectl get deployments,pods,services
kubectl describe deployment shop-api
kubectl logs deployment/shop-api
```

The Kubernetes manifest is a learning configuration. The API uses in-memory demo
data, so orders and inventory reset when a pod restarts and are not shared between
replicas. A real system would use a shared persistent database.

## GitHub Actions

The workflow runs tests, builds an image tagged with the commit SHA, and scans it
with Trivy. The final deployment job is deliberately a placeholder; it does not
perform a real deployment. Configure a real deployment target and secrets before
claiming automated deployment.

## Incident runbook: CrashLoopBackOff

1. `kubectl get pods -o wide` — identify affected replicas and nodes.
2. `kubectl describe pod <pod>` — inspect events, exit code, probes and termination reason.
3. `kubectl logs <pod> --previous` — inspect the last crashed container's logs.
4. Check configuration, image, command, resource limits and dependency connectivity.
5. If a new rollout caused the outage, `kubectl rollout undo deployment/shop-api`.
6. Verify with `kubectl rollout status deployment/shop-api` and `kubectl get endpoints shop-api`.

## Limitations

This repository is intended for learning. It does not include production authentication,
persistent storage, secrets management, ingress/TLS, or a real deployment target.
Do not use it to process real customer data.
