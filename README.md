# EVM Tracker

Herramienta para que los líderes de proyecto registren el avance de sus actividades y vean, con
**Valor Ganado (Earned Value Management)**, si el proyecto va bien o mal en cronograma y presupuesto.

| Capa | Tecnología |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2, PostgreSQL 16 |
| Frontend | React 19, Vite, TypeScript (`strict`), servido con nginx |
| Calidad | ruff, mypy `strict`, pytest + cobertura ≥ 80 %, oxlint, Prettier |

El plan de implementación y las decisiones de diseño están en [docs/PLAN.md](docs/PLAN.md).

## Requisitos

- Docker con Docker Compose v2.
- Solo para desarrollo sin Docker: Python 3.12 con [uv](https://docs.astral.sh/uv/) y Node.js 22 o superior.

## Correr el proyecto con Docker

```bash
docker compose up -d --build
```

Levanta tres servicios. Cada uno espera a que el anterior esté sano:

| Servicio | URL | Descripción |
|---|---|---|
| `web` | http://localhost:8080 | Dashboard. nginx redirige `/api` al backend |
| `api` | http://localhost:8000 | API REST. Swagger en http://localhost:8000/api-docs |
| `db` | `localhost:5434` | PostgreSQL con el esquema y el proyecto de demostración |

- Estado de los servicios: `docker compose ps` (los tres deben verse `healthy`).
- Salud del API: `GET http://localhost:8000/health` responde `{"status": "ok", "database": "up"}`.
- Swagger también está disponible desde el front: http://localhost:8080/api-docs.

Los puertos y las credenciales se pueden cambiar copiando `.env.example` a `.env`. La base se publica
en el **5434** para no chocar con un PostgreSQL instalado localmente en el 5432.

### Base de datos

Los scripts de [db/init/](db/init/) se ejecutan **solo la primera vez** que se crea el volumen:

- `01_schema.sql`: tablas, restricciones `CHECK` (BAC > 0, porcentajes entre 0 y 100, AC ≥ 0) y
  borrado en cascada de actividades.
- `02_seed.sql`: proyecto de demostración "Portal de clientes" (fecha de corte 2026-10-03) con 3 actividades.

Para reiniciar la base desde cero (borra los datos):

```bash
docker compose down -v
```

## Desarrollo local

### Backend

```bash
cd backend
uv sync
cp .env.example .env
uv run uvicorn app.main:create_app --factory --reload
```

`.env.example` apunta a la base `db` de docker-compose (`docker compose up -d db`).

| Variable | Obligatoria | Descripción |
|---|---|---|
| `DATABASE_URL` | Sí | Cadena SQLAlchemy, p. ej. `postgresql+psycopg://evm:evm@localhost:5434/evm` |
| `APP_NAME` | No | Título del API en Swagger |
| `APP_VERSION` | No | Versión publicada en Swagger |
| `TEST_DATABASE_URL` | No (solo pruebas) | Base de integración. Por defecto, `db-test` en el puerto 5433 |

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite sirve en http://localhost:5173 y redirige `/api` a `http://localhost:8000`. Para cambiar el destino,
define `API_PROXY_TARGET`.

## Pruebas y calidad

Las pruebas de integración usan una base **aislada** (`db-test`, puerto 5433, solo esquema y datos en
memoria). Nunca tocan la base de la demo.

```bash
docker compose --profile test up -d --wait db-test
```

Backend (desde `backend/`):

```bash
uv run pytest
```

```bash
uv run ruff check .
```

```bash
uv run ruff format --check .
```

```bash
uv run mypy app tests
```

`pytest` falla si la cobertura baja del 80 %.

Frontend (desde `frontend/`):

```bash
npm run typecheck
```

```bash
npm run lint
```

```bash
npm run format:check
```

## Estructura

```
backend/    API FastAPI (app/) y pruebas (tests/)
frontend/   SPA React + configuración de nginx
db/init/    Esquema y seed de PostgreSQL
docs/       Plan de implementación
```
