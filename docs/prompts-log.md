<!-- Copia idéntica de la sección 2 de AI_PROCESS.md. Si cambias una, cambia la otra. -->

## 2. Prompts (textuales y en orden cronológico)

**Ubicación del log:** en este documento. `docs/prompts-log.md` es una copia idéntica de esta sección.
**Reinicios o sesiones exploratorias:** `se realizaron sesiones exploratorias en tres diferentes IA para tener contexto. Esos prompts están al final, en la sección "Prompts de otra IA".`

### Prompt #1
- **Fecha / hora:** `2026-10-03 21:17`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `aprendizaje`

````text
@"C:\Users\juand\Downloads\Ingeniero de Desarrollo — Trycore Colombia.pdf"


Adjunto el enunciado de una prueba técnica.

Objetivo: que tengas el contexto completo antes de planear. No escribas código todavía.

Entrégame:
1. Un resumen de lo que se pide (backend, frontend, estándares y entregables).
2. Los criterios de evaluación, ordenados por peso.
3. Las ambigüedades del enunciado que convendría aclarar con Trycore.
````

- **Qué hizo la IA (una línea):** `Leyó el PDF y entregó el resumen, los criterios ordenados por peso (aclarando que el enunciado no da porcentajes) y 19 ambigüedades agrupadas por tema.`
- **Qué hice yo con eso:** `adopté` · ` lo adopte porque es la primera parte de darle contexto a la ia para que funcione sin ningun problema.`

### Prompt #2
- **Fecha / hora:** `2026-10-03 21:19`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `aprendizaje`

````text
No conozco Earned Value Management. Explícamelo como a un ingeniero que nunca lo ha usado:
1. La idea central con una analogía.
2. Qué responde cada indicador del enunciado (PV, EV, CV, SV, CPI, SPI, EAC, VAC).
3. Las relaciones que siempre deben cumplirse entre ellos.
4. Qué pasa matemáticamente en los casos borde: AC = 0, PV = 0, EV = 0, proyecto sin actividades.

Después dame un ejercicio con datos para que yo lo calcule a mano; no me des la respuesta hasta que te envíe mis resultados.
````

- **Qué hizo la IA (una línea):** `Explicó EVM con la analogía de pintar 10 cuartos, la pregunta que responde cada indicador, las relaciones y los casos borde, y dejó el ejercicio "Portal de clientes" (A–D) sin respuesta.`
- **Qué hice yo con eso:** `adopté` · `con respecto a la investigación de las demas IA y en la web encontre que no era un tema sencillo de explicar por lo cual teniendo un ejercicio donde yo solucione y la IA revise me ayuda a segurar no solo que entendi el ejercicio bien, sino que tambien estamos en la misma pagina con respecto al contexto.`

### Prompt #3
- **Fecha / hora:** `2026-10-03 21:23`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `aprendizaje`

````text
Estos son mis resultados del ejercicio.

1. CÁLCULO POR ACTIVIDAD
(montos en millones de pesos, CPI y SPI a 4 decimales)

A. Diseño (BAC 20, plan 100 %, real 100 %, AC 18)
PV = 1,00 x 20 = 20
EV = 1,00 x 20 = 20
CV = EV - AC = 20 - 18 = +2
SV = EV - PV = 20 - 20 = 0
CPI = EV / AC = 20 / 18 = 1,1111
SPI = EV / PV = 20 / 20 = 1,0000
EAC = BAC / CPI = 20 / 1,1111 = 18
VAC = BAC - EAC = 20 - 18 = +2

B. Desarrollo (BAC 50, plan 60 %, real 40 %, AC 25)
PV = 0,60 x 50 = 30
EV = 0,40 x 50 = 20
CV = 20 - 25 = -5
SV = 20 - 30 = -10
CPI = 20 / 25 = 0,8000
SPI = 20 / 30 = 0,6667
EAC = 50 / 0,8 = 62,5
VAC = 50 - 62,5 = -12,5

C. Pruebas (BAC 10, plan 20 %, real 30 %, AC 2)
PV = 0,20 x 10 = 2
EV = 0,30 x 10 = 3
CV = 3 - 2 = +1
SV = 3 - 2 = +1
CPI = 3 / 2 = 1,5000
SPI = 3 / 2 = 1,5000
EAC = 10 / 1,5 = 6,6667
VAC = 10 - 6,6667 = +3,3333

D. Despliegue (BAC 8, plan 0 %, real 0 %, AC 0)
PV = 0 x 8 = 0
EV = 0 x 8 = 0
CV = 0 - 0 = 0
SV = 0 - 0 = 0
CPI = 0 / 0 = indefinido (N/A)
SPI = 0 / 0 = indefinido (N/A)
EAC = N/A (depende del CPI)
VAC = N/A (depende del EAC)

2. INTERPRETACIÓN POR ACTIVIDAD

A. Diseño: bajo presupuesto, porque CPI 1,1111 es mayor a 1 (gasté 18 para lograr 20 de valor). A tiempo, porque SPI es exactamente 1 (avancé lo que había planificado).
B. Desarrollo: sobre presupuesto, porque CPI 0,8000 es menor a 1 (gasté 25 para lograr 20 de valor). Atrasada, porque SPI 0,6667 es menor a 1 (llevo 20 de los 30 que debía tener).
C. Pruebas: bajo presupuesto, porque CPI 1,5000 es mayor a 1 (gasté 2 para lograr 3 de valor). Adelantada, porque SPI 1,5000 es mayor a 1 (llevo 3 de los 2 que debía tener).
D. Despliegue: no aplicable. Todavía no ha empezado, por eso CPI y SPI no están definidos.

3. CONSOLIDADO DEL PROYECTO
Primero sumo los montos y después calculo los índices sobre esas sumas. No promedio los índices.

BAC total = 20 + 50 + 10 + 8 = 88
PV = 20 + 30 + 2 + 0 = 52
EV = 20 + 20 + 3 + 0 = 43
AC = 18 + 25 + 2 + 0 = 45

CV = 43 - 45 = -2
SV = 43 - 52 = -9
CPI = 43 / 45 = 0,9556
SPI = 43 / 52 = 0,8269
EAC = 88 / 0,9556 = 92,0930 (exacto: 88 x 45 / 43)
VAC = 88 - 92,0930 = -4,0930

Interpretación: el proyecto está sobre presupuesto (CPI menor a 1) y atrasado (SPI menor a 1).

4. PREGUNTAS DE RAZONAMIENTO

a) ¿El EAC del proyecto es igual a la suma de los EAC de las actividades? ¿Por qué?
No.
Suma de A + B + C = 18 + 62,5 + 6,6667 = 87,1667
Si incluyo D con su BAC (8) = 95,1667
EAC del proyecto = 92,0930
El EAC del proyecto aplica un solo CPI global (0,9556) a todo el presupuesto de 88. La suma usa el CPI propio de cada actividad y además no puede estimar D. Son dos estimaciones con supuestos distintos, no una identidad.
También comprobé que el promedio simple de los CPI de A, B y C es (1,1111 + 0,8000 + 1,5000) / 3 = 1,1370, que diría "bajo presupuesto". El CPI correcto del proyecto es 0,9556 (sobre presupuesto). El promedio invierte el veredicto porque le da el mismo peso a Pruebas (AC de 2) que a Desarrollo (AC de 25).

b) ¿Qué haría con los indicadores de D y cómo afecta D al consolidado?
En D, PV, EV, CV y SV dan 0, pero CPI y SPI son 0 / 0, y EAC y VAC tampoco se pueden calcular porque dependen del CPI. No los mostraría como 0, porque 0 diría "pésimo" cuando en realidad significa "aún no hay datos". Los mostraría como N/A (null con estado NOT_APPLICABLE en la API).
En el consolidado, D suma 0 a PV, EV y AC, así que no cambia el CPI ni el SPI. Sí suma 8 al BAC total, y eso sube el EAC: asume que D se ejecutará con la misma eficiencia que el resto del proyecto. Sin D, el EAC sería 80 / 0,9556 = 83,7209. D agrega 8 / 0,9556 = 8,3721, y 83,7209 + 8,3721 = 92,0930.

c) En una frase, como se lo diría a un gerente:
"El proyecto va mal: está sobre presupuesto y atrasado (por cada peso gastado producimos 96 centavos de valor, y llevamos 83 centavos de avance por cada peso planificado), y si seguimos así terminará costando unos 92,1 millones en vez de 88, con el problema concentrado en Desarrollo."

5. VERIFICACIÓN DE RELACIONES
CV y CPI: A es + con CPI mayor a 1; B es - con CPI menor a 1; C es + con CPI mayor a 1; proyecto es - con CPI menor a 1. Se cumple.
SV y SPI: A es 0 con SPI = 1; B es - con SPI menor a 1; C es + con SPI mayor a 1; proyecto es - con SPI menor a 1. Se cumple.
VAC y CV: A es + y +; B es - y -; C es + y +; proyecto es - y -. Se cumple.
VAC = BAC - EAC en todas las filas. Se cumple.
EAC x CPI = BAC: B = 62,5 x 0,8 = 50; proyecto = 92,0930 x 0,9556 = 88. Se cumple.
CPI del proyecto como promedio ponderado por AC: (1,1111 x 18 + 0,8 x 25 + 1,5 x 2) / 45 = 43 / 45. Se cumple.
D queda fuera de las relaciones de signo porque sus índices no están definidos.
````

- **Qué hizo la IA (una línea):** `Revisó línea por línea: todos los números correctos; señaló el redondeo intermedio (18,0002), el supuesto CPI = 1 escondido al sumar D, los distintos tipos de "indefinido" y que el PMI tiene otras fórmulas de EAC.`
- **Qué hice yo con eso:** `adopté` · `es la revisión del ejercicio para estar seguros que tanto la IA como yo tenemos la misma cantidad de conocimiento del proyecto.`

### Prompt #4
- **Fecha / hora:** `2026-10-03 21:25`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `aprendizaje`

````text
¿Cómo se consolidan los indicadores de varias actividades a nivel de proyecto? Compara promediar los CPI contra calcular ΣEV/ΣAC con un contraejemplo numérico donde den veredictos opuestos.
````

- **Qué hizo la IA (una línea):** `Separó lo que se suma de lo que se recalcula y dio dos contraejemplos (promedio 1,25 frente a ΣEV/ΣAC 0,5149, y 0,875 frente a 1,2407), con el argumento de que dividir una actividad no debe cambiar el CPI.`
- **Qué hice yo con eso:** `adopté` · `hice una pregunta en donde las IA no simpre respondieron con claridad al momento de realizar la busqueda, luego de esto valide la respuesta de la IA.`

### Prompt #5
- **Fecha / hora:** `2026-10-03 21:26`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `plan`

````text
Con el contexto anterior, vamos a planear la solución.

Decisiones que ya tomé:
- Backend: Python 3.12 + FastAPI + SQLAlchemy 2 + PostgreSQL 16. Frontend: React + Vite + TypeScript strict.
- Arquitectura por capas con el dominio EVM como funciones puras, sin dependencias del framework.
- Los indicadores se calculan al leer; no se persisten.
- Gitflow: main, develop, una rama feature/* por funcionalidad con PR, y release/1.0.0.

Objetivo: un plan en docs/PLAN.md con estructura de carpetas, modelo de datos, contrato del API (endpoints, códigos de error), estrategia de pruebas, ramas y cronograma para una jornada de 10 horas.

Restricción: para cada decisión, indica la alternativa descartada y el porqué. Si alguna de mis decisiones te parece débil, cuestiónala.
````

- **Qué hizo la IA (una línea):** `Escribió docs/PLAN.md con cada decisión y su alternativa descartada; cuestionó "calcular al leer" sin Decimal ni redondeo al presentar, y que a Gitflow le faltaban el back-merge y el tag; propuso un motivo por cada índice no disponible y montos como número JSON.`
- **Qué hice yo con eso:** `modifiqué` · `aunque el plan de la IA aceptable, tome lagunas decisiones del stack tecnologico para que fuera mucho mas efectivo y rapido al momento de desarrollar y generar pruebas.  `

### Prompt #6
- **Fecha / hora:** `2026-10-03 21:29`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `plan`

````text
Revisé el plan. Ajustes:
- Reduce las ramas feature a 6: scaffolding, motor EVM, API, frontend dashboard, visualización EVM y documentación. Más release/1.0.0.
- CI queda opcional, solo si sobra tiempo.
- Para las pruebas de integración, una base de datos aislada en docker-compose en lugar de testcontainers.
- Hypothesis: máximo 3 propiedades, con estrategias acotadas a donde cada invariante está definido (AC > 0, %plan > 0).
- Frontend: 3,5 horas, formulario en modal y una sola gráfica.

Actualiza docs/PLAN.md con estos cambios.
````

- **Qué hizo la IA (una línea):** `Actualizó PLAN.md: 6 ramas más release, CI fuera del cronograma, db-test en docker-compose, las 3 propiedades P1–P3 con sus rangos y el frontend en 3,5 h; señaló que P3 también exige %real > 0.`
- **Qué hice yo con eso:** `adopté` · `La IA acepeto mi plan para comenzar el desarrollo de manera ordenada. `

### Prompt #7
- **Fecha / hora:** `2026-10-03 21:38`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `plan`

````text
Iniciamos la implementación según docs/PLAN.md. Repositorio local: "D:\trycore test\EVM-test-" y el repositorio de GitHub: https://github.com/jdcastellanosb73/EVM-test-

Flujo de trabajo: tú escribes el código; yo reviso cada cambio y hago los commits. Por cada módulo entrégame un mensaje de commit en inglés, en imperativo, con un cuerpo en viñetas que detalle lo que se añade.

Objetivo: rama feature/project-scaffolding con:
- db/init: esquema con NUMERIC para dinero y restricciones CHECK, más un seed de demostración: proyecto "Portal de clientes" (fecha de corte 2026-10-03) con 3 actividades:
  | Actividad | BAC | % plan | % real | AC |
  | Diseño UX | 8000000 | 100 | 100 | 7200000 |
  | Desarrollo backend | 20000000 | 60 | 45 | 12000000 |
  | Pruebas QA | 6000000 | 20 | 0 | 0 |
- backend: FastAPI con /health y Swagger en /api-docs; configuración por variables de entorno; ruff, mypy strict y pytest con cobertura mínima de 80 %.
- frontend: Vite + React + TS strict, oxlint y Prettier; nginx con proxy a /api.
- docker-compose: db, api, web y db-test (perfil test, puerto 5433, solo esquema).
- README con instrucciones para correr el proyecto en local.

Criterio de aceptación: lint, tipos y pruebas en verde, y `docker compose up` con los tres servicios sanos.
````

- **Qué hizo la IA (una línea):** `Creó develop y feature/project-scaffolding con el esquema, el seed, FastAPI con /health contra la base, el front, nginx, docker-compose y el README; verificó lint, tipos, 6 pruebas y los tres servicios sanos, y entregó 5 mensajes de commit.`
- **Qué hice yo con eso:** `adopté` · `creo la base del proyecto.`

### Prompt #8
- **Fecha / hora:** `2026-10-03 21:53`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `motor`

````text
Rama feature/evm-calculation-engine. Escribe primero las pruebas y luego el código.

Reglas de negocio:
1. AC = 0 → CPI null con estado NOT_APPLICABLE; EAC y VAC también null.
2. EV = 0 con AC > 0 → CPI = 0 (valor real, OVER_BUDGET); EAC y VAC null.
3. PV = 0 → SPI null con NOT_APPLICABLE.
4. Proyecto sin actividades → totales en 0, índices null.
5. El proyecto se consolida con la razón de sumas, nunca promediando índices; debe reutilizar la misma función de cálculo de una actividad.
6. Precisión completa con Decimal; redondeo solo al presentar: dinero 2 decimales, índices 4, ROUND_HALF_UP en una constante.
7. El estado se decide con el valor sin redondear (caso borde: CPI 0,99996 → "1.0000" con OVER_BUDGET).
8. Validación en el dominio: BAC > 0, porcentajes entre 0 y 100, AC ≥ 0.

Pruebas: valores calculados a mano (el ejemplo del enunciado y el dataset de demo), cada caso borde verificando índice, estado y EAC/VAC, el contraejemplo del promedio, y 3 propiedades con Hypothesis.

Criterio de aceptación: 100 % de cobertura del dominio, sin números mágicos.
````

- **Qué hizo la IA (una línea):** `Escribió primero las pruebas (fallaron porque el módulo no existía) y luego el motor puro; 46 pruebas del dominio al 100 % de cobertura; calculó EAC como BAC × AC / EV y pidió que verificara a mano los valores del dataset de demo.`
- **Qué hice yo con eso:** `adopté` · `en este momento al principio estaba por rechazarlo, sin embargo al revisar que las fallas fueron porque el modulo no existia, una vez se realizo valide manualmente los valores del dataset que usamos de demo y al ver que pasaban se adopto la respuesta.`

### Prompt #9
- **Fecha / hora:** `2026-10-03 22:08`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `operativo`

````text
ayudame con los commits porfa que me esta fallando al subir el commit de cada una de las cosas
````

- **Qué hizo la IA (una línea):** `Encontró que no había ningún commit y que estaba en la rama equivocada; hizo los 8 commits (5 de scaffolding y 3 del motor) a mi nombre, sin co-autor, con git commit -F, y comprobó las pruebas en una copia temporal.`
- **Qué hice yo con eso:** `modifiqué ` · `Al usar la herramienta de github desktop este genero fallas, al momento de generar el commit, debido a que en una sesión anterior tuve errores con estos debido a la ia, esta vez tome una pausa para asegurar de que cada uno de los commits los hiciera yo en la rama pertinente y no tener errores.`

### Prompt #10
- **Fecha / hora:** `2026-10-03 22:14`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `frontend`

````text
Rama feature/frontend-dashboard.

Objetivo: lista de proyectos con semáforo de CPI/SPI y detalle del proyecto con tabla de actividades y formulario en modal para crear y editar.

Restricciones: TanStack Query; al guardar, los indicadores se refrescan. El frontend no calcula EVM: muestra lo que entrega el API. Los montos se formatean con Intl.NumberFormat a partir del string.
````

- **Qué hizo la IA (una línea):** `Revisó el repositorio, vio que el API del que depende el dashboard todavía no existía y preguntó si hacer el API primero; rechacé la pregunta e interrumpí (22:15) para enviar el prompt #11.`
- **Qué hice yo con eso:** `rechacé` · `debido a un error al momento de realizar el plan que se habia planteado me salte un paso y le solicite realizar el front al notar que faltaba el backend para que funcionara de manera correcta y no tener que volver para conectar el front con el back opte por cancelarlo para seguir el plan.`

### Prompt #11
- **Fecha / hora:** `2026-10-03 22:15`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `API`

````text
Rama feature/projects-activities-api.

Objetivo: CRUD de proyectos y actividades y consolidado EVM según el contrato de docs/PLAN.md.

Restricciones:
- Controladores delgados: la lógica vive en services y en el dominio.
- Dinero e índices viajan como string en el JSON, para que el frontend no pierda precisión.
- Formato de error único {code, message, details}; 404 y 422 documentados en OpenAPI con descripción y esquemas.
- Al menos una prueba de integración por endpoint contra db-test, validando el contrato: campos monetarios como str, comparados con Decimal, nunca con float. Incluye los 422 por BAC ≤ 0, % fuera de rango y AC < 0.
````

- **Qué hizo la IA (una línea):** `Implementó modelos ORM, servicios, routers delgados y el formato de error único; 89 pruebas validadas contra el esquema OpenAPI; actualizó PLAN.md (montos como string, NOT_APPLICABLE, error plano) y dejó 6 mensajes de commit.`
- **Qué hice yo con eso:** `adopté` · `revise el codigo y estaba funcionando sin ningun problema, aparte de esto yo subo los commits y sigue el plan de trabajo.`

### Prompt #12
- **Fecha / hora:** `2026-10-03 22:29`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `frontend`

````text
Rama feature/frontend-dashboard.

Objetivo: lista de proyectos con semáforo de CPI/SPI y detalle del proyecto con tabla de actividades y formulario en modal para crear y editar.

Restricciones: TanStack Query; al guardar, los indicadores se refrescan. El frontend no calcula EVM: muestra lo que entrega el API. Los montos se formatean con Intl.NumberFormat a partir del string.
````

- **Qué hizo la IA (una línea):** `Construyó la lista con semáforo, el detalle con tabla y totales, y el modal de crear y editar; lo probó en el navegador y corrigió el scroll horizontal, el Location sin puerto detrás de nginx y los mensajes del API en inglés.`
- **Qué hice yo con eso:** `adopté` · `teniendo el servicio del back levantado en el backend realice una prueba mediante postman validando todo lo entregado una vez validado su funcionamiento continue con el plan.`

### Prompt #13
- **Fecha / hora:** `2026-10-03 22:52`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `frontend`

````text
Rama feature/evm-visualization.

Objetivo: tarjetas de CPI, SPI, EAC y VAC con color y una frase legible; gráfica de barras agrupadas PV/EV/AC por actividad con Recharts.

Restricción: la etiqueta y el color acompañan siempre al número, para que un CPI de 0,996 mostrado como "1,00" no se lea como "en presupuesto".
````

- **Qué hizo la IA (una línea):** `Antes de empezar avisó que los commits del dashboard no estaban hechos y preguntó cómo seguir (ver #14); después hizo las tarjetas con frases que dependen del estado del API y la gráfica PV/EV/AC (leyenda ordenada, nombres que se ajustan en móvil, carga diferida).`
- **Qué hice yo con eso:** `rechaze` · `opte por continuar mientras hacia los commits, sin embargo trabajar sobre la rama y no una nueva generaria errores por lo cual rechace el prompt y realice los commits.`

### Prompt #14
- **Fecha / hora:** `2026-10-03 22:54`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5` · respuesta escrita en la pregunta de selección de la IA
- **Fase:** `operativo`

````text
ya los acabo de hacer
````

- **Qué hizo la IA (una línea):** `Comprobó en git que los 6 commits del dashboard estaban subidos y creó feature/evm-visualization encima.`
- **Qué hice yo con eso:** `adopté` · `informarle a claude que los commits estaban realizados que no tendriamos ningun problema continuando con el trabajo.`

### Prompt #15
- **Fecha / hora:** `2026-10-03 23:06`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `verificación`

````text
@"C:\Users\juand\Downloads\evm_ejercicio_v2.xlsx"
Construí un Excel con las mismas fórmulas para el dataset de demo.
Compáralos con la respuesta del API para el proyecto demo e identifica cualquier diferencia y su causa.
````

- **Qué hizo la IA (una línea):** `Encontró que el Excel tenía el dataset del ejercicio A–D y no el del demo (9 de 40 coincidían); con los mismos datos coincidieron 40 de 40 y 50 de 50, y las únicas diferencias residuales fueron de redondeo, dentro de la tolerancia.`
- **Qué hice yo con eso:** ` modifiqué ` · `subi un archivo que no era por lo cual las coincidencias eran minimas 9/40 en este caso opte por hacerlo a malo y revisarlo con lo que me dieron una vez validado fue aceptado.`

### Prompt #16
- **Fecha / hora:** `2026-10-03 23:09`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `operativo`

````text
Voy a escribir AI_PROCESS.md. Dame una estructura con las secciones que exige el enunciado y, para cada una, preguntas guía que me ayuden a redactarla con mis palabras. No redactes las respuestas: la reflexión debe ser mía.
```

> Cuando termines de escribirlo, completa la bitácora hasta el último prompt enviado e integra el PR de documentación a `develop` antes de la release.
````

- **Qué hizo la IA (una línea):** `Dio 7 secciones con preguntas guía sin redactar respuestas; no ejecutó la nota final (completar la bitácora e integrar el PR) porque era para después y afectaba al repositorio remoto.`
- **Qué hice yo con eso:** `modifique` · `tome algunos campos que me sugeria la IA otros los continue debido a que no tenia todo el contexto de todo lo que se hizo en otras IA.`

### Prompt #17
- **Fecha / hora:** `2026-10-03 23:18`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `operativo`

````text
Prepara release/1.0.0: revisa el README (instrucciones completas para correr el proyecto en local), verifica que no haya código comentado ni variables sin usar, y dame la checklist para el merge a main y el tag v1.0.0.
````

- **Qué hizo la IA (una línea):** `Revisó el código con ruff, vulture, tsc, oxlint y knip (solo 2 exports de más, corregidos) y empezó a probar el README con un clon limpio desde GitHub; la prueba se cortó porque Docker Desktop se detuvo.`
- **Qué hice yo con eso:** `adopté` · `se realiza una validación de todo el funcionamiento para asegurar de que todo funciona sin ningun problema para genera el release.`

### Prompt #18
- **Fecha / hora:** `2026-10-04 00:04`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `operativo`

````text
Intentar nuevamente
````

- **Qué hizo la IA (una línea):** `Reinició Docker Desktop, repitió la prueba del clon limpio (Docker, 89 pruebas de backend, front y build), completó el README y entregó la checklist hacia main y v1.0.0, explicando que la release no se podía crear porque faltaban los PR.`
- **Qué hice yo con eso:** `adopté` · `Fallo la conexión con claude nuevamente esto genero que la respuesta se cortara al hacer esto claude me permite enviar intentar nuevamente para repetir la ultima pregunta enviada`

### Prompt #19
- **Fecha / hora:** `2026-10-04 17:29`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `operativo`

````text
estoy trabajando en la parte de AI_Process.md y estoy en este punto me puedes ayudar dandome cada uno de los prompts en este formato: 


## 2. Prompts (textuales y en orden cronológico)

> Guía: copia cada prompt tal cual lo enviaste, sin resumir ni corregir. Incluye los exploratorios, los reinicios y los operativos (commits, errores, formato). Si hubo varias sesiones o herramientas, ordénalas por fecha y hora. Si el log es muy largo, puedes moverlo a `docs/prompts-log.md` y enlazarlo aquí, pero sigue siendo parte de la entrega.

**Ubicación del log:** `<en este documento / docs/prompts-log.md>`
**Reinicios o sesiones exploratorias:** `<cómo los marcaste>`

Formato de cada entrada:

### Prompt #1
- **Fecha / hora:** `…`
- **Herramienta:** `…`
- **Fase:** `aprendizaje | plan | motor | API | frontend | verificación | operativo`

```text
<pega aquí el prompt exacto>
```

- **Qué hizo la IA (una línea):** `…`
- **Qué hice yo con eso:** `adopté | modifiqué | rechacé` · `<por qué, en una línea>`
````

- **Qué hizo la IA (una línea):** `Extrajo los prompts de las transcripciones de la sesión con fecha y hora, y armó este log textual en docs/prompts-log.md, dejando para mí la columna "Qué hice yo con eso".`
- **Qué hice yo con eso:** `adopté` · `esto se hizo con el fin de responder el punto 2 del ejercicio.`


### Prompt #20
- **Fecha / hora:** `2026-10-04 20:44`
- **Herramienta:** `Claude Code (app de escritorio, pestaña Code) · Claude Opus 5.5`
- **Fase:** `verificación`

````text
@"C:\Users\juand\Downloads\Ingeniero de Desarrollo — Trycore Colombia.pdf"
revisemos que no falte nada de lo que nos pidieron, actualmente solo falta el gitflow, revisemos que esto este en orden para pasar a  gitflow. 

cosas para tener en cuenta : Prueba evalúa EVM; se requiere 80% cobertura pruebas unitarias y Gitflow estricto.
````

- **Qué hizo la IA (una línea):** `Revisó el enunciado punto por punto y corrió todas las pruebas (100 de backend con 99,85 % de cobertura, 27 de frontend, linters y build); encontró que el comando del README para comprobar el 100 % del dominio fallaba (medía toda la app).`
- **Qué hice yo con eso:** `adopté` · `quería entrar al Gitflow sabiendo que ningún commit intermedio rompe las pruebas.`
