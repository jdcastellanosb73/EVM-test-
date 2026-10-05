# EVM Tracker

Herramienta para que los líderes de proyecto registren el avance de sus actividades y vean, con
**Valor Ganado (Earned Value Management)**, si el proyecto va bien o mal en cronograma y presupuesto.

| Capa | Tecnología |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2, PostgreSQL 16 |
| Frontend | React 19, Vite, TypeScript (`strict`), TanStack Query, React Router, Recharts; servido con nginx |
| Calidad | ruff, mypy `strict`, pytest + Hypothesis + cobertura ≥ 80 %, contrato OpenAPI validado con jsonschema, Vitest, oxlint, Prettier |

| Documento | Contenido |
|---|---|
| [docs/PLAN.md](docs/PLAN.md) | Plan de implementación y decisiones de diseño, cada una con su alternativa descartada |
| [AI_PROCESS.md](AI_PROCESS.md) | Proceso de trabajo con IA: herramientas, prompts, aprendizaje de EVM y verificación |
| http://localhost:8000/api-docs | Contrato del API (OpenAPI / Swagger), con el stack corriendo |

## Requisitos

- Docker con Docker Compose v2.
- Solo para desarrollo sin Docker: Python 3.12 con [uv](https://docs.astral.sh/uv/) y Node.js 22 o superior.

## Inicio rápido (Docker)

```bash
git clone https://github.com/jdcastellanosb73/EVM-test-.git
```

```bash
cd EVM-test-
```

```bash
docker compose up -d --build
```

La primera vez tarda unos minutos porque construye las imágenes. Levanta tres servicios; cada uno espera
a que el anterior esté sano:

| Servicio | URL | Descripción |
|---|---|---|
| `web` | http://localhost:8080 | Dashboard. nginx redirige `/api` al backend |
| `api` | http://localhost:8000 | API REST. Swagger en http://localhost:8000/api-docs |
| `db` | `localhost:5434` | PostgreSQL con el esquema y el proyecto de demostración |

- Estado de los servicios: `docker compose ps` (los tres deben verse `healthy`).
- Salud del API: `GET http://localhost:8000/health` responde `{"status": "ok", "database": "up"}`.
- Swagger también está disponible desde el front: http://localhost:8080/api-docs.

**Qué deberías ver** en http://localhost:8080: el proyecto "Portal de clientes" con CPI **0,8854 · Sobre
presupuesto** y SPI **0,8019 · Atrasado**. Al abrirlo aparecen las tarjetas de CPI, SPI, EAC y VAC, la
gráfica PV/EV/AC por actividad y la tabla de actividades, donde se pueden crear, editar y eliminar.

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

Necesita la base de datos corriendo:

```bash
docker compose up -d db
```

Desde `backend/`:

```bash
uv sync
```

```bash
cp .env.example .env
```

En PowerShell, el equivalente es `Copy-Item .env.example .env`. `.env.example` ya apunta a la base `db` de
docker-compose (puerto 5434).

```bash
uv run uvicorn app.main:create_app --factory --reload
```

El API queda en http://localhost:8000 y Swagger en http://localhost:8000/api-docs.

| Variable | Obligatoria | Descripción |
|---|---|---|
| `DATABASE_URL` | Sí | Cadena SQLAlchemy, p. ej. `postgresql+psycopg://evm:evm@localhost:5434/evm` |
| `APP_NAME` | No | Título del API en Swagger |
| `APP_VERSION` | No | Versión publicada en Swagger |
| `TEST_DATABASE_URL` | No (solo pruebas) | Base de integración. Por defecto, `db-test` en el puerto 5433 |

### Frontend

Necesita el API corriendo en el puerto 8000, ya sea con `uv run uvicorn …` o con
`docker compose up -d db api`. Desde `frontend/`:

```bash
npm install
```

```bash
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

`pytest` falla si la cobertura baja del 80 %. La capa de dominio (cálculo EVM) está al 100 %:

```bash
uv run pytest tests/unit --cov-reset --cov=app/domain --cov-fail-under=100
```

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

```bash
npm test
```

## Solución de problemas

| Síntoma | Causa y solución |
|---|---|
| `port is already allocated` al levantar | Otro programa usa el puerto. Copia `.env.example` a `.env` y cambia `DB_PORT`, `API_PORT` o `WEB_PORT` |
| No aparece el proyecto de demostración | Los scripts de `db/init/` solo corren al crear el volumen. Reinicia la base con `docker compose down -v` |
| Los cambios de código no se ven en Docker | Las imágenes se construyen una vez; vuelve a levantar con `docker compose up -d --build` |
| Las pruebas de integración fallan al conectar | Falta la base aislada: `docker compose --profile test up -d --wait db-test` |

## Estructura

```
backend/
  app/domain/evm/   Motor EVM: funciones puras, sin framework ni base de datos
  app/services/     Casos de uso: CRUD y cálculo de indicadores al leer
  app/api/          Routers delgados, esquemas del contrato y formato de error
  app/db/           Engine, sesión y modelos ORM
  tests/            Unitarias (dominio) e integración (API contra db-test)
frontend/
  src/api/          Cliente HTTP tipado y hooks de TanStack Query
  src/features/     Lista de proyectos, detalle, actividades y gráfica
  src/lib/          Formato de montos, semáforo y lectura de indicadores
db/init/            Esquema (01) y seed de demostración (02)
docs/               Plan, bitácora de prompts y Excel de validación EVM
AI_PROCESS.md       Proceso de trabajo con IA
```
