# Plan de implementación — EVM Tracker

Herramienta interna para registrar el avance de las actividades de un proyecto y analizarlo con Valor Ganado (EVM).
Cada decisión trae la alternativa descartada y el motivo.

## 1. Decisiones base (revisadas)

| # | Decisión | Alternativa descartada | Motivo |
|---|---|---|---|
| D1 | Python 3.12 + FastAPI + SQLAlchemy 2 (**síncrono**) + PostgreSQL 16 | SQLAlchemy async + asyncpg | La carga es de unas pocas filas por request. Async complica las sesiones y los fixtures de prueba sin ganancia medible. |
| D2 | React + Vite + TypeScript `strict` | Angular | Hay más dominio en React. Para un dashboard de una pantalla, Angular agrega estructura sin aportar. |
| D3 | Dominio EVM como funciones puras, sin dependencias de FastAPI ni SQLAlchemy | Lógica en los modelos ORM o en los servicios | El enunciado exige cubrir la lógica EVM con pruebas unitarias. Si es pura, se prueba sin base de datos ni mocks. |
| D4 | Indicadores **calculados al leer**, nunca persistidos | Columnas `pv`, `ev`, `cpi`… actualizadas al guardar | Persistirlos duplica datos derivados, y pueden quedar desactualizados si alguien edita una fila por fuera del API. El costo de recalcular es despreciable. |
| D5 | **`Decimal` en el dominio**, `NUMERIC` en PostgreSQL | `float` | Son montos de dinero. Con `float`, 0,1 + 0,2 ≠ 0,3 y las relaciones como EAC × CPI = BAC fallarían en las pruebas por ruido binario. |
| D6 | Redondear **solo en la frontera del API** (2 decimales para montos, 4 para índices) | Redondear en el dominio | El redondeo intermedio se propaga: 20 / 1,1111 da 18,0002 en lugar de 18. Se comprobó en el ejercicio manual. |
| D7 | Una sola función calcula los indicadores a partir de `(BAC, PV, EV, AC)`. El consolidado es la misma función aplicada a las sumas | Una función por actividad y otra por proyecto | Evita duplicar fórmulas. Además, promediar índices da veredictos invertidos (el contraejemplo queda como prueba en §8). |
| D8 | Gitflow con PR reales en GitHub, *merge commit* (`--no-ff`), `release/1.0.0` → `main` por PR, tag `v1.0.0` y **back-merge a `develop`** | *Squash merge* y merges locales | El historial es parte de la entrega: el *squash* lo aplanaría, y un merge local no deja PR. El back-merge faltaba en la decisión original y Gitflow lo exige. |

### Cuestionamientos a las decisiones originales

- **"Calcular al leer"** es sólida, pero estaba incompleta: sin D5 y D6, calcular al leer con `float` produce números que no cuadran con el cálculo a mano.
- **Gitflow:** faltaban el back-merge y el tag. Además, este mismo `PLAN.md` no debe entrar por commit directo a `main`: va en `feature/project-scaffolding`.
- **"Funciones puras"** debe incluir también la **interpretación** y los **casos borde** (por qué un índice no está disponible). Si eso queda en el controlador o en el front, la lógica de negocio se dispersa.
- **Faltaban decisiones:**
  - la escala de los porcentajes (D9);
  - cómo se inicializa la BD (D11);
  - con qué base corren las pruebas de integración (§8).

## 2. Supuestos sobre las ambigüedades del enunciado

Se documentan en el README. Si Trycore responde, se ajustan.

| # | Supuesto | Alternativa descartada | Motivo |
|---|---|---|---|
| D9 | El API recibe y entrega porcentajes en escala **0–100**. El dominio los convierte a fracción con la constante `PERCENT_SCALE` | Escala 0–1 en el API | 0–100 es como lo escribe el líder de proyecto. La conversión vive en un solo lugar. |
| D10 | La **fecha de corte** es un campo del proyecto (informativo). El % planificado se ingresa a mano | Calcular el % planificado a partir de fechas de inicio y fin | El enunciado define el % planificado como dato de entrada y no pide fechas por actividad. |
| — | Validaciones: `BAC > 0`; `0 ≤ %plan, %real ≤ 100`; `AC ≥ 0`. Se permite AC > 0 con avance 0 | Rechazar AC > 0 con avance 0 | Gastar sin avanzar es justo la alerta que EVM debe mostrar, no un error de entrada. |
| — | CPI y SPI = 1 exacto se interpretan como "en presupuesto" y "a tiempo". Sin banda de tolerancia | Banda configurable (0,95–1,05) | El enunciado solo define mayor o menor que 1. Se deja como mejora futura. |
| — | Borrar un proyecto borra sus actividades (`ON DELETE CASCADE`). El front pide confirmación | 409 si el proyecto tiene actividades | Una actividad no existe sin su proyecto. Un 409 obliga a borrar fila por fila sin aportar nada. |
| — | Sin autenticación: herramienta interna de un solo usuario | Login por líder de proyecto | El enunciado no lo pide y no aporta a lo que se evalúa. |
| — | "Tiempo real" significa que, al guardar una actividad, la tabla, el consolidado y la gráfica se recalculan sin recargar la página | Calcular en vivo en el front mientras se escribe | Exigiría duplicar las fórmulas en TypeScript, con dos fuentes de verdad que pueden divergir. |

## 3. Estructura de carpetas

```
EVM-test-/
├── backend/
│   ├── app/
│   │   ├── domain/evm/            # PURO: sin FastAPI ni SQLAlchemy
│   │   │   ├── values.py          # EarnedValueBase, EvmIndicators, PerformanceIndex (dataclasses frozen)
│   │   │   ├── calculator.py      # calculate_indicators(base), consolidate(bases)
│   │   │   ├── interpretation.py  # clasificación de CPI y SPI contra 1
│   │   │   └── constants.py       # PERCENT_SCALE, PERFORMANCE_BASELINE = 1
│   │   ├── services/              # casos de uso: orquestan la BD y el dominio
│   │   │   ├── project_service.py
│   │   │   └── activity_service.py
│   │   ├── db/                    # engine, sesión y modelos ORM
│   │   ├── api/
│   │   │   ├── routers/           # projects.py, activities.py (sin lógica de negocio)
│   │   │   ├── schemas/           # Pydantic: request y response
│   │   │   └── errors.py          # excepciones de dominio → respuesta de error estándar
│   │   ├── config.py              # pydantic-settings
│   │   └── main.py                # app, routers, handlers, /api-docs
│   ├── tests/
│   │   ├── unit/domain/           # cálculo, consolidado, casos borde, propiedades
│   │   └── integration/api/       # un test o más por endpoint, contra PostgreSQL real
│   └── pyproject.toml             # ruff, mypy, pytest, coverage
├── frontend/
│   └── src/
│       ├── api/                   # cliente HTTP tipado
│       ├── features/projects/     # lista y selector de proyecto
│       ├── features/activities/   # tabla y formulario modal (crear y editar)
│       ├── components/            # IndicatorCard, StatusBadge, EvmChart
│       └── types/                 # contratos del API
├── db/
│   └── init/
│       ├── 01_schema.sql          # esquema: fuente de verdad (db y db-test)
│       └── 02_seed.sql            # proyecto de demo "Portal de clientes" (solo db)
├── docs/                          # PLAN.md, prompts-log.md
├── .github/workflows/ci.yml       # OPCIONAL: solo si sobra tiempo (§10)
├── docker-compose.yml             # db (5434), db-test (5433, aislada, tmpfs), api
├── README.md
└── AI_PROCESS.md
```

| # | Decisión | Alternativa descartada | Motivo |
|---|---|---|---|
| D12 | Servicios que usan la `Session` directamente, **sin capa de repositorios** | Patrón Repository con interfaces | Con 2 entidades y CRUD simple, el repositorio solo agrega indirección. Probarlo con mocks no prueba nada real: los servicios se prueban con integración contra PostgreSQL. La lógica que sí vale la pena aislar ya está pura en `domain/`. |

## 4. Modelo de datos

```sql
CREATE TABLE projects (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name         VARCHAR(120) NOT NULL UNIQUE,
    description  VARCHAR(500),
    cutoff_date  DATE,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE activities (
    id                    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_id            BIGINT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name                  VARCHAR(120) NOT NULL,
    budget_at_completion  NUMERIC(15,2) NOT NULL CHECK (budget_at_completion > 0),
    planned_percent       NUMERIC(5,2)  NOT NULL CHECK (planned_percent BETWEEN 0 AND 100),
    actual_percent        NUMERIC(5,2)  NOT NULL CHECK (actual_percent BETWEEN 0 AND 100),
    actual_cost           NUMERIC(15,2) NOT NULL CHECK (actual_cost >= 0),
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (project_id, name)
);
CREATE INDEX ix_activities_project_id ON activities(project_id);
```

| # | Decisión | Alternativa descartada | Motivo |
|---|---|---|---|
| D11 | `db/init/01_schema.sql` es la fuente de verdad del esquema. PostgreSQL lo ejecuta al iniciar (`docker-entrypoint-initdb.d`) y las pruebas de integración lo aplican a `db-test` | Alembic | El enunciado pide literalmente un script de inicialización, y hay un solo esquema sin historia. Como las pruebas corren contra ese mismo script, cualquier desajuste con los modelos ORM rompe la suite. Alembic entraría cuando el esquema evolucione. |
| — | Validación en dos niveles: Pydantic (422 con mensaje claro) y `CHECK` en la BD (última barrera) | Solo Pydantic | Los `CHECK` protegen ante cualquier escritura que no pase por el API. |
| — | IDs `BIGINT IDENTITY` | UUID | Herramienta interna: los IDs legibles facilitan la demo y la depuración, y no hay riesgo de enumeración que mitigar. |

## 5. Dominio EVM

```python
ActivityProgress(bac, planned_percent, actual_percent, ac)   # valida al construirse
EarnedValueBase(bac, pv, ev, ac)                             # 4 montos Decimal, sumables
calculate_indicators(base) -> EvmIndicators                  # bac, pv, ev, ac, cv, sv, cpi, spi, eac, vac
calculate_activity_indicators(progress) -> EvmIndicators
consolidate_project_indicators(activities) -> EvmIndicators  # = calculate_indicators(suma de las bases)
```

- **Índices** (`PerformanceIndex`): `value: Decimal | None` y `status`.
  - Estados del CPI: `UNDER_BUDGET` · `ON_BUDGET` · `OVER_BUDGET` · `NOT_APPLICABLE`.
  - Estados del SPI: `AHEAD_OF_SCHEDULE` · `ON_SCHEDULE` · `BEHIND_SCHEDULE` · `NOT_APPLICABLE`.
  - El estado se decide con el valor **sin redondear**: CPI 0,99996 se muestra como `1.0000` pero es `OVER_BUDGET`.
- **Casos borde** (reglas implementadas en `feature/evm-calculation-engine`):

| Caso | Resultado |
|---|---|
| AC = 0 | CPI `null`, `NOT_APPLICABLE`. EAC y VAC `null` |
| EV = 0 y AC > 0 | CPI = 0 (valor real) → `OVER_BUDGET`. EAC y VAC `null` (BAC / 0) |
| PV = 0 | SPI `null`, `NOT_APPLICABLE` |
| Proyecto sin actividades | Montos en 0. CPI, SPI, EAC y VAC `null` |

| # | Decisión | Alternativa descartada | Motivo |
|---|---|---|---|
| — | Un índice no disponible es `null` con estado `NOT_APPLICABLE` | Devolver 0, 1 o infinito | 0 dice "pésimo" y 1 dice "perfecto": ambos inventan un dato. Infinito no es serializable en JSON. |
| — | Un solo estado `NOT_APPLICABLE`, sin motivo | Un motivo por caso (`NO_DATA`, `NO_ACTUAL_COST`, `NO_PLANNED_VALUE`, `ZERO_PERFORMANCE`), propuesto en la primera versión de este plan | Decisión del desarrollador al fijar las reglas del motor (ver `AI_PROCESS.md`). Los montos que explican el caso (AC, EV, PV) viajan en la misma respuesta. |
| — | EAC = BAC / CPI, calculado como BAC × AC / EV | Dividir por el CPI ya calculado | Es la misma fórmula del enunciado, pero no divide por un cociente ya redondeado. La propiedad EAC × CPI = BAC lo verifica. |
| — | EAC = BAC / CPI, la fórmula del enunciado | Otras fórmulas del PMI, como AC + (BAC − EV) | El enunciado la fija. Las demás se mencionan en el `AI_PROCESS.md` como alternativa considerada. |

## 6. Contrato del API

Base: `/api/v1`. Documentación OpenAPI en **`/api-docs`**: cada endpoint lleva descripción, esquemas y respuestas de error declaradas.

| Método | Ruta | Éxito | Errores |
|---|---|---|---|
| GET | `/projects` | 200: lista con el consolidado de cada proyecto | — |
| POST | `/projects` | 201 + `Location` | 409 `PROJECT_NAME_TAKEN`, 422 |
| GET | `/projects/{project_id}` | 200: proyecto + actividades con indicadores + consolidado (todo el dashboard en una llamada) | 404 `PROJECT_NOT_FOUND` |
| PUT | `/projects/{project_id}` | 200 | 404, 409, 422 |
| DELETE | `/projects/{project_id}` | 204 (borra sus actividades en cascada) | 404 |
| GET | `/projects/{project_id}/activities` | 200: actividades con indicadores | 404 |
| POST | `/projects/{project_id}/activities` | 201 + `Location` | 404, 409 `ACTIVITY_NAME_TAKEN`, 422 |
| GET | `/projects/{project_id}/activities/{activity_id}` | 200 | 404 `PROJECT_NOT_FOUND` / `ACTIVITY_NOT_FOUND` |
| PUT | `/projects/{project_id}/activities/{activity_id}` | 200 | 404, 409, 422 |
| DELETE | `/projects/{project_id}/activities/{activity_id}` | 204 | 404 |
| GET | `/health` | 200 | — |

Formato de error único para todo 4xx, incluido el 422 (se reemplaza el *handler* de FastAPI) y las rutas inexistentes:

```json
{ "code": "VALIDATION_ERROR", "message": "Request validation failed",
  "details": [ { "field": "body.budget_at_completion", "message": "Input should be greater than 0" } ] }
```

Bloque de indicadores, el mismo para actividad y proyecto. Dinero, porcentajes e índices viajan como **string**:

```json
{ "bac": "50000000.00", "pv": "30000000.00", "ev": "20000000.00", "ac": "25000000.00",
  "cv": "-5000000.00", "sv": "-10000000.00",
  "cpi": { "value": "0.8000", "status": "OVER_BUDGET" },
  "spi": { "value": "0.6667", "status": "BEHIND_SCHEDULE" },
  "eac": "62500000.00",
  "vac": "-12500000.00" }
```

| # | Decisión | Alternativa descartada | Motivo |
|---|---|---|---|
| — | Rutas anidadas `/projects/{id}/activities/{id}` | Rutas planas `/activities/{id}` | Pedir una actividad por fuera de su proyecto da 404. La pertenencia queda en el contrato. |
| — | `PUT` con el recurso completo | `PATCH` parcial | El formulario siempre envía todos los campos. PATCH agrega casos (campos ausentes vs. null) sin ningún uso. |
| — | Dinero, porcentajes e índices como **string decimal** ya redondeado (dinero 2 decimales, índices 4) | Número JSON | Un número JSON se lee en el front como `float` binario y puede perder precisión. El string conserva el valor exacto; el front lo convierte solo para graficar. Esta decisión reemplaza la de la primera versión del plan. |
| — | Prefijo `/api/v1` | Sin versión | Es barato y deja espacio para cambios de contrato. |
| — | Formato de error plano `{code, message, details}` | Envoltorio `{"error": {...}}` | Es el formato definido por el desarrollador; el envoltorio no aporta información. |

## 7. Frontend

- **Una pantalla:**
  - selector y CRUD de proyectos;
  - 4 tarjetas de consolidado (CPI, SPI, EAC, VAC) con badge de color y texto ("Sobre presupuesto");
  - tabla de actividades con sus indicadores; crear y editar en un **formulario modal**;
  - **una sola gráfica**: barras agrupadas PV / EV / AC por actividad.
- **Tras cada mutación** se vuelve a pedir `GET /projects/{id}`. No hay cálculo en el front.
- **Presupuesto de tiempo:** 3,5 h en total (dashboard 2 h 45 min + gráfica 45 min).

| Decisión | Alternativa descartada | Motivo |
|---|---|---|
| Formulario en modal, compartido por crear y editar | Edición en línea en la tabla | El modal se valida y se envía como una unidad, y un solo componente sirve para los dos casos. La edición en línea exige manejar el estado celda por celda y no cabe en 3,5 h. |
| Una sola gráfica (PV / EV / AC por actividad) | Gráficas adicionales (curva S, evolución del CPI) | Es la única que pide el enunciado. Una curva S requeriría historial de cortes, que no se persiste (D10). |
| TanStack Query para leer e invalidar | `useEffect` + `fetch` a mano | La invalidación tras guardar es el "tiempo real" pedido, y viene resuelta con estados de carga y error. |
| Recharts | Chart.js, ECharts | Es declarativa, se integra con React y alcanza para barras agrupadas. |
| Proxy de Vite hacia el API en desarrollo | Configurar CORS | No hay orígenes cruzados en local: menos configuración y menos superficie. |
| Color **más** texto y valor en los estados | Solo color | Accesibilidad. Además, "se entiende de un vistazo" exige que diga qué significa. |

## 8. Estrategia de pruebas

| Nivel | Qué | Herramienta |
|---|---|---|
| Unitarias del dominio | **Caso de referencia:** el ejercicio "Portal de clientes" (A–D) calculado a mano, con todos los indicadores por actividad y consolidados | pytest parametrizado |
| | Casos borde de §5: AC = 0, PV = 0, EV = 0 y proyecto sin actividades, verificando valor, estado **y** motivo | pytest |
| | **Consolidado:** el contraejemplo donde el promedio de CPI da 1,25 y ΣEV / ΣAC da 0,5149. La prueba fija que se usan las sumas | pytest |
| | **Propiedades (máximo 3)**, cada una con estrategias acotadas al dominio donde el invariante está definido (ver la tabla siguiente) | Hypothesis |
| Integración | Cada endpoint, tanto el éxito como su error principal. El cuerpo **se valida contra el esquema OpenAPI** del propio app, para que el contrato documentado y el real no puedan divergir | pytest + TestClient + jsonschema, contra `db-test` |
| Cobertura | `--cov=app/domain --cov=app/services --cov-fail-under=80` (meta: dominio al 100 %) | pytest-cov |
| Estática | ruff (lint y formato), mypy `strict` en `domain/`, `tsc --noEmit` y ESLint en el front | En local antes de cada PR; en CI solo si sobra tiempo |

**Propiedades con Hypothesis.** Los montos se generan como `Decimal` con 2 decimales y los porcentajes en 0–100. Cada propiedad acota además sus estrategias al rango donde su invariante está definido. Lo que queda fuera de ese rango (AC = 0, PV = 0, EV = 0) no se genera aleatoriamente: lo cubren las pruebas de casos borde, con valores fijos.

| # | Invariante | Estrategia acotada a | Por qué ese rango |
|---|---|---|---|
| P1 | CV > 0 ⇔ CPI > 1, CV = 0 ⇔ CPI = 1, CV < 0 ⇔ CPI < 1 | AC > 0 | Con AC = 0, el CPI no existe |
| P2 | SV > 0 ⇔ SPI > 1, SV = 0 ⇔ SPI = 1, SV < 0 ⇔ SPI < 1 | %plan > 0 (con BAC > 0, implica PV > 0) | Con PV = 0, el SPI no existe |
| P3 | EAC × CPI = BAC (con tolerancia de redondeo) y signo(VAC) = signo(CV) | AC > 0 y %real > 0 | Con EV = 0, el CPI vale 0 y el EAC = BAC / 0 no existe |

La propiedad "consolidar = calcular sobre las sumas" queda como prueba de ejemplo con el contraejemplo de consolidación; no se repite como propiedad.
| Front | Mapeo de estado a etiqueta y color, y formato de montos | Vitest |

| Decisión | Alternativa descartada | Motivo |
|---|---|---|
| Integración contra PostgreSQL real, una transacción con rollback por prueba | SQLite en memoria | SQLite trata distinto `NUMERIC`, `CHECK` y `ON DELETE CASCADE`. Las pruebas pasarían con una base que no es la de producción. |
| Base aislada `db-test` declarada en `docker-compose.yml`: puerto 5433, datos en `tmpfs` y esquema cargado desde el mismo `01_schema.sql` (sin seed) | Testcontainers | Es la misma imagen y el mismo esquema que la base de la demo, sin otra dependencia en el proyecto. Se levanta con un comando documentado en el README. Al estar separada de `db` (5434), las pruebas nunca tocan los datos de la demo. |
| Pruebas que comprueban **valores** calculados a mano | Pruebas que solo verifican que la respuesta tenga campos | El enunciado penaliza explícitamente las pruebas que "solo verifican que las funciones retornan algo". |

## 9. Ramas y PR

| Orden | Rama | Contenido | PR a |
|---|---|---|---|
Seis ramas `feature/*` más la `release`:

| Orden | Rama | Contenido | PR a |
|---|---|---|---|
| 0 | `develop` | Se crea desde `main` | — |
| 1 | `feature/project-scaffolding` | Estructura, docker-compose (`db` + `db-test`), `db/init/` (esquema + seed de demo), `/health`, Swagger, linters, este plan | `develop` |
| 2 | `feature/evm-calculation-engine` | Motor EVM puro: cálculo, consolidado, interpretación, casos borde, pruebas unitarias y Hypothesis | `develop` |
| 3 | `feature/projects-activities-api` | Sesión de BD, CRUD de proyectos y actividades, indicadores en las respuestas, formato de errores, `/api-docs` e integración por endpoint | `develop` |
| 4 | `feature/dashboard-ui` | Front: proyectos, tabla de actividades, formulario modal, tarjetas de consolidado y badges | `develop` |
| 5 | `feature/evm-visualization` | Gráfica PV / EV / AC por actividad | `develop` |
| 6 | `feature/documentation` | README final y `AI_PROCESS.md` | `develop` |
| 7 | `release/1.0.0` | Versión, ajustes finales (solo correcciones) | `main`, luego tag `v1.0.0` y back-merge a `develop` |

- Si sobra tiempo, el CI (`.github/workflows/ci.yml`) entra en su propia rama `feature/ci-pipeline` antes de la release.

- Commits en imperativo y en inglés (`Add EVM calculation service`, `Handle zero actual cost in CPI`).
- Cada PR lleva una descripción con qué cambia y cómo se probó.

## 10. Cronograma (jornada de 10 h)

| Hora | Bloque | Entregable verificable |
|---|---|---|
| Hora | Bloque (rama) | Entregable verificable |
|---|---|---|
| 0:00–0:45 | Scaffolding | `docker compose up db db-test` levanta las dos bases con el esquema, y la de demo con el seed |
| 0:45–2:15 | Motor EVM | Caso de referencia, casos borde y P1–P3 en verde. Cobertura del dominio al 100 % |
| 2:15–4:15 | API | CRUD de proyectos y actividades con su integración por endpoint. Los indicadores de `GET /projects/{id}` son iguales al cálculo a mano. `/api-docs` navegable |
| 4:15–4:30 | Pausa | — |
| 4:30–7:15 | Dashboard | Crear, editar y borrar con el modal; el consolidado y la tabla se recalculan al guardar |
| 7:15–8:00 | Visualización | Gráfica PV / EV / AC del proyecto "Portal de clientes" |
| 8:00–8:20 | Verificación de punta a punta | Los números de la UI cuadran con el ejercicio a mano, incluido D |
| 8:20–8:50 | Documentación | README; `AI_PROCESS.md` completado (los prompts se registran **desde ya**, no al final) |
| 8:50–9:15 | Release | PR `release/1.0.0` → `main`, tag, back-merge |
| 9:15–10:00 | Video | Guion en viñetas (no leído), ensayo y grabación de 10 min o menos |

- Total del frontend: 3,5 h (4:30–8:00).
- **CI:** opcional y fuera del cronograma. Entra solo si algún bloque termina antes de tiempo.

**Si el tiempo aprieta**, se recorta en este orden:
1. Vitest del front.
2. Hypothesis (las relaciones P1–P3 quedan como pruebas de ejemplo con valores fijos).

**No se recortan:** pruebas del dominio, integración por endpoint, `AI_PROCESS.md` y video. Son lo que más pesa en la evaluación.

## 11. Proceso con IA (insumo para el AI_PROCESS.md)

- `docs/prompts-log.md` se actualiza **en cada prompt, textual y en orden**. El enunciado penaliza el documento genérico "escrito después del hecho".
- Se anotan en el momento, no de memoria al final:
  - las sugerencias de la IA que se descartaron;
  - las validaciones hechas a mano, como el ejercicio A–D y los contraejemplos de consolidación.
