# Kubernetes Manifests

This directory contains the Kubernetes configuration for running Infigrate.
It uses Kustomize so shared resources live in `base/`, while environment-specific
settings live in `development/` and `production/`.

## Deploying

```sh
kubectl apply -k k8s/development
kubectl apply -k k8s/production
```

The cluster must have Gateway API CRDs installed and a Gateway controller with
the `GatewayClass` referenced by the selected environment.

## Directory Layout

### `base/`

`base/` contains the shared Kubernetes resources used by every environment.
These files should define the common shape of the system without committing to
environment-specific values like hostnames, replica counts, image tags, or
storage sizes.

- `kustomization.yml`: Lists the shared resources that make up the base.
- `api.yml`: Defines the FastAPI API `Deployment`, internal `Service`,
  `Gateway`, and `HTTPRoute`.
- `postgres.yml`: Defines the Postgres `Secret`, `StatefulSet`, persistent
  volume claim template, and internal `Service`.
- `queue.yml`: Defines the Redis `StatefulSet`, persistent volume claim
  template, and internal `Service`.

### `development/`

`development/` is the overlay for developer and non-production deployments.
It deploys into the `infigrate-dev` namespace.

- `kustomization.yml`: Pulls in `../base`, sets the namespace, sets the API
  image tag to `development`, and applies development patches.
- `namespace.yml`: Creates the `infigrate-dev` namespace.
- `api-deployment-patch.yml`: Sets development API deployment details, including
  a single replica and local-friendly image pull behavior.
- `api-gateway-patch.yml`: Sets the development Gateway host and
  `GatewayClass`.
- `api-route-patch.yml`: Sets the development API route hostname.
- `postgres-secret-patch.yml`: Sets development Postgres database credentials.
- `postgres-storage-patch.yml`: Sets development Postgres storage size.
- `queue-storage-patch.yml`: Sets development Redis storage size.

### `production/`

`production/` is the overlay for production deployments. It deploys into the
`infigrate-prod` namespace.

- `kustomization.yml`: Pulls in `../base`, sets the namespace, sets the API
  image tag to `production`, and applies production patches.
- `namespace.yml`: Creates the `infigrate-prod` namespace.
- `api-deployment-patch.yml`: Sets production API deployment details, including
  higher replica count and always pulling the configured image tag.
- `api-gateway-patch.yml`: Sets the production Gateway host and `GatewayClass`.
- `api-route-patch.yml`: Sets the production API route hostname.
- `postgres-secret-patch.yml`: Sets production Postgres values. Replace the
  placeholder password before deploying.
- `postgres-storage-patch.yml`: Sets production Postgres storage size.
- `queue-storage-patch.yml`: Sets production Redis storage size.

## Traffic Flow

External HTTP traffic enters through the environment's Gateway API `Gateway`.
The `HTTPRoute` sends matching requests to the `infigrate-api` `Service`, which
forwards traffic to API pods on port `8000`.

Inside the cluster, the API connects to:

- Postgres through the `postgres` service on port `5432`.
- Redis through the `redis` service on port `6379`.

## Production Notes

Before deploying production, update:

- The API image repository and tag.
- The production `GatewayClass`.
- The production hostname.
- The Postgres password in `production/postgres-secret-patch.yml`, or replace
  that Secret with your cluster's secret-management approach.
