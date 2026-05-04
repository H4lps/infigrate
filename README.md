# infigrate

## Development

This workspace uses `uv` for Python package management.

```sh
uv --cache-dir .uv-cache sync
```

Add runtime dependencies with `uv --cache-dir .uv-cache add <package>` and
development-only dependencies with `uv --cache-dir .uv-cache add --dev <package>`.

## Services

Local development uses PostgreSQL for the database and Redis for the message
queue.

```sh
cp .env.example .env
docker compose up -d postgres redis
```

## Kubernetes

Kubernetes manifests live in `k8s/` and use Kustomize overlays.

```sh
kubectl apply -k k8s/development
kubectl apply -k k8s/production
```

The shared resources are in `k8s/base`. Development deploys into
`infigrate-dev`, and production deploys into `infigrate-prod`.

The API uses Gateway API resources for external HTTP traffic. Update each
environment's host, `gatewayClassName`, API image tag, and production Postgres
secret before deploying. Your cluster must have Gateway API CRDs installed and
a Gateway controller that provides the referenced `GatewayClass`.
