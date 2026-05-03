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
