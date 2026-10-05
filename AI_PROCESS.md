# AI_PROCESS.md

Prueba técnica Trycore Colombia: herramienta de Valor Ganado (EVM).
Autor: `Juan Diego Castellanos` · Repositorio: `https://github.com/jdcastellanosb73/EVM-test-` · Fecha de entrega: `04/10/2026` (desarrollo del 03/10/2026 al 04/10/2026)



---

## 1. Herramientas de IA y por qué las elegí

| Herramienta | Para qué la usé | Por qué esa y no otra |
|---|---|---|
|v0|La use para mejorar el diseño de la entrega|V0 es la una ia especializada en diseños, por lo cual me parece una herarmienta muy buena para diseños del front de manera rapida y efectiva.|
|Claude code|Es mi herramienta de trabajo directo, con esta herramienta realice gran parte del proyecto-|Opte por esta herramienta, puesto que como es mi herramienta de trabajo del dia a dia ya contiene mi contexto de forma de trabajar y tambien mis skill, rules y me permite de manera facil crear subagentes para tareas en especifico.|
|chat GTP, Claude y copilot|use estas herramientas para enterarme de que se trataba el proyecto y entenderlo para poder solucionar sin ningun problema. |estas herramientas son las que mas se usan con fines de conocimiento y busqueda opte por estas ya que me sirven para dar la información y compararlas entre ellas para estar seguro, no es toma de decisiones en donde pueden tender a darle la razón al usuario para generar ese sentimiento de que el usuario siempre tiene la razón.| 

**Qué decidí no hacer con IA, y por qué:**
`Las decisiones tomadas y todos los ejercicios de entendimiento se realizaron sin ayuda de la IA, es decir la ia me dio el ejercicio y ya con el fin de tener un entendimiento al 100% de lo que pedia el problema y de lo que se necesitaba, esto debido a que si no tengo el conocimiento del funcionamiento de proyecto no puedo entender el codigo y/o fallas en la logica y estaria dependiendo 100% de la IA.`

**Cómo nos repartimos el trabajo** (quién escribía código, quién revisaba, quién hacía los commits, y por qué lo organicé así):
`Con la IA decidi realizar gran parte del proyecto, lo primero que hice fue darle el pdf a la ia con el fin de que tuviera el contexto, en este momento tambien opte por pasarlo como texto directo ya que consume menos tokens, pero como tengo una skill para que pueda leer pdfs, le pedi que lo leyera para bajar el margen de error, una vez lo leyo y estaba seguro de que funcionaria el paso 2 fue darle el contexto, esto lo hice mediante pregunta para que me explicara su funcionamiento y tambien estuvieramos a la par en conocimiento y contexto. ahora para estar seguros que resolveriamos lo mismo le pedi a claude un ejercicio para resolverlo donde el tambien tenia que resolverlo y revisar mis respuestas para encontrar errores. Una vez tenia en cuenta que la IA ya tenia el contexto igual que yo, decidi optar por un plan de trabajo, este plan luego de verlo decidi mejorarlo mediante un prompt comentandole mis decisiones de igual manera para tener un mejor panorama si alguna decision fuera mala le pedi a claude que me comentara cuando algo no tenia sentido o existia un caso mejor y el porque. Luego de esto nos dividimos el trabajo en una vez teniendo las reglas de negocio claras por parte de ambos el realizaba el codigo, yo revisaba el codigo y con ayuda de subagentes haciamos pruebas en tiempo real. los commits se dividieron 50/50 esto debido a que en un intento claude fallo con el uso de ramas y daño todo el proceso y adelanto que tenia, por este motivo aunque claude creaba la rama y el pr yo revisaba los commits y realizaba los commits para estar seguro de todo lo que se hacia y se subia. de tal manera de mantener el orden que pedia el ejercicio sin necesidad de romper el ejercicio y el orden hasta un punto donde consumia mas tokens arreglarlo que reiniciar el proyecto.`
---

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


## 3. Cómo aprendí EVM

**Qué sabía y qué no sabía antes de empezar:**
`Entiendo que EVM sirve para comparar presupuesto es decir el avance real con respecto al presupuesto real, no conocia ninguna de sus formulas y no recuerdo qué significan PV, EV y AC ni cómo se calculan CPI y SPI. Tampoco sé cómo se juntan varias actividades para sacar el resultado de todo el proyecto.`

**Qué le pregunté primero a la IA y por qué en ese orden:**
Primero pedí una explicación completa desde cero, con analogía, qué responde cada
indicador, las relaciones que siempre se cumplen y los casos borde (AC = 0, PV = 0,
EV = 0, proyecto sin actividades). Empecé por ahí porque no recordaba el tema y quería
un mapa completo antes de calcular. Segundo, pedí un ejercicio para resolver a mano sin
que me diera la respuesta, para comprobar que entendía antes de implementar. Al final
pregunté por la consolidación, porque es lo que menos se deduce de las fórmulas por
actividad y donde más fácil es equivocarse.



**Qué parte me costó más entender y qué me ayudó:**
Lo más difícil fue la consolidación: entender por qué el CPI del proyecto no es el
promedio de los CPI de las actividades. Me ayudó el contraejemplo numérico donde ambos
métodos dan veredictos opuestos, porque mostró que el promedio ignora cuánto dinero
pesa cada actividad. También me ayudó comparar con mi forma de entenderlo
("¿por qué no funciona así?") para ver exactamente dónde fallaba mi razonamiento.

**Validación antes de implementar**

- Ejercicio que resolví a mano (datos y fecha): `el demo que solicite a claude para que ambos estuvieramos en la misma pagina`
- Dónde acerté: `acerte en los calculos de CV, SV, CPI y SPI`
- Dónde me corrigió la IA (con el valor o el razonamiento concreto): `la IA me corrigio mucho al momento de repasar conocimientos ya que muchas veces no tenia seguro como se compartan las metricas de los casos borde. `
- Cómo comprobé que entendía la **consolidación** del proyecto, no solo las fórmulas por actividad (por ejemplo: promedio de CPI frente a ΣEV/ΣAC, y por qué el EAC del proyecto no es la suma de los EAC): `realice una consulta a claude con respectoa  esa duda del promedio de CPI frente a ΣEV/ΣAC en caso de no estar seguro de la respuesta de claude y/o no tener claridad hubiera preguntando con un: pero porque no funciona de esta manera : (la manera en la que yo lo entendía) con el fin de notar la diferencia.`
- Qué puedo explicar hoy sin mirar notas, y qué todavía no domino: ``
Puedo explicar sin notas qué miden PV, EV y AC, cómo se leen CPI y SPI (>1 o <1), por qué el CPI del proyecto se calcula con ΣEV/ΣAC y no promediando, y qué pasa en los casos borde: con AC = 0 el CPI no existe y por eso tampoco el EAC ni el VAC; con avance real 0 y costo registrado el CPI es 0 de verdad (sobre presupuesto) y el EAC no se puede calcular; con 0 % planificado el SPI no existe; y un proyecto sin actividades queda con los montos en 0 y los índices sin calcular. Lo que todavía no domino es cuándo conviene cada variante de EAC que usa el PMI (por ejemplo, AC + (BAC − EV) cuando el desvío fue puntual); en la app usé EAC = BAC / CPI porque es la que fija el enunciado.

**Evidencia:** 

- Prompts: #2 (explicación de EVM desde cero, con casos borde, y ejercicio sin respuesta), #3 (mis
  resultados del ejercicio a mano) y #4 (consolidación: promedio de CPI vs ΣEV/ΣAC). Están textuales en
  la sección 2.
- Ejercicio a mano: mis cálculos están en el prompt #3. `docs/evm_ejercicio_v2.xlsx` es ese mismo ejercicio,
  que armé yo con las fórmulas del enunciado.

---


## 4. Dos decisiones en las que no seguí a la IA

### Decisión 1: Plan recortado (6 ramas, CI opcional y db-test en lugar de Testcontainers)
- **Qué propuso la IA** (prompt #5): un PLAN.md con más de 6 ramas feature, CI dentro del cronograma y Testcontainers para las pruebas de integración.
- **Qué hice yo en su lugar** (prompt #6): reduje a 6 ramas feature más `release/1.0.0`, dejé el CI como opcional solo si sobraba tiempo, usé una base aislada `db-test` en docker-compose en lugar de Testcontainers, limité Hypothesis a 3 propiedades con estrategias acotadas y fijé el frontend en 3,5 horas con formulario en modal y una sola gráfica.
- **Por qué:** tenía una jornada de 10 horas y quería el camino más rápido y efectivo para desarrollar y generar pruebas. `db-test` usa la misma imagen y el mismo `01_schema.sql` que la base de la demo, así que Testcontainers solo agregaba otra dependencia.
- **Qué costo o riesgo acepté:** sin CI, nadie detecta regresiones automáticamente: corro lint, tipos y pruebas en local antes de cada PR. Las pruebas de integración exigen levantar `db-test` con un comando del README y son menos herméticas que con Testcontainers.
- **Dónde se ve en el repo:** `docs/PLAN.md` §8 (decisión de `db-test`), §9 (ramas y CI en rama propia si sobra tiempo) y §10; servicio `db-test` en `docker-compose.yml`.

### Decisión 2: Dinero, porcentajes e índices como string en el JSON
- **Qué propuso la IA** (prompt #5): montos como número JSON. La bitácora de #5 lo registra y el PLAN.md actual lo confirma ("reemplaza la de la primera versión").
- **Qué hice yo en su lugar** (prompt #11): exigí que dinero e índices viajen como string decimal ya redondeado (2 decimales para dinero, 4 para índices), y la IA actualizó el PLAN.md.
- **Por qué:** el dominio calcula con `Decimal`. Un número JSON se lee en JavaScript como float y puede perder precisión, justo donde la regla de negocio depende del redondeo. Con string, el frontend formatea con `Intl.NumberFormat` sin calcular EVM, y las pruebas comparan con `Decimal`, nunca con float.
- **Qué costo o riesgo acepté:** el contrato es menos directo para quien consuma el API, porque hay que convertir strings. El frontend solo convierte a número para graficar con Recharts, y ahí acepto la pérdida de precisión.
- **Dónde se ve en el repo:** `docs/PLAN.md` §6 (bloque de indicadores y fila de decisión), el esquema en `/api-docs`, las pruebas de integración de contrato (campos monetarios como `str`).

---

## 5. Cómo verifiqué que los números tienen sentido

**Valores calculados a mano y dónde quedaron:** Calculé a mano las 3 actividades y el total del proyecto (Diseño UX, Desarrollo backend, Pruebas QA, PROYECTO) y los pasé a `docs/EVM_demo.xlsx`. Ejemplo: Desarrollo backend, BAC 20.000.000, PV = 20M × 60 % = 12.000.000, EV = 20M × 45 % = 9.000.000, AC 12.000.000 → CV = −3.000.000, SV = −3.000.000, CPI = SPI = 0,75, EAC = 20M / 0,75 = 26.666.666,67.

**Relaciones entre indicadores que usé para revisar:**
- Signos: CV > 0 ⇔ CPI > 1 y SV > 0 ⇔ SPI > 1. Diseño UX: CV = +800.000 y CPI = 1,11. Backend: CV y SV negativos con CPI y SPI = 0,75. QA: SV = −1.200.000 con SPI = 0.
- VAC = BAC − EAC: UX 8M − 7,2M = 800.000; Backend 20M − 26,67M = −6.666.666,67; Proyecto 34M − 38,4M = −4.400.000.
- EAC × CPI = BAC: Backend 26.666.666,67 × 0,75 = 20.000.000; Proyecto 38,4M × 0,8854 = 34.000.000.
- ETC = EAC − AC: Proyecto 38,4M − 19,2M = 19,2M.
- Ratio de sumas vs. promedio: el CPI del proyecto es ΣEV / ΣAC = 17M / 19,2M = 0,8854, no el promedio de los CPI de las actividades. SPI proyecto = 17M / 21,2M = 0,8019. Un promedio simple daría un SPI de 0,58 (promedio de 1, 0,75 y 0), que es claramente incorrecto: las actividades pesan distinto.

**Casos borde que verifiqué:**

| Caso | Qué esperaba | Qué obtuve |
|---|---|---|
| AC = 0 | CPI = N/A (no dividir por 0). EAC, ETC y VAC también N/A porque dependen del CPI. | Pruebas QA (AC = 0): CPI, EAC y VAC = `null` en la API y N/A en Excel; COINCIDE. Estado de costo: NOT_APPLICABLE. Prueba unitaria: `test_zero_actual_cost_with_progress_makes_cpi_eac_and_vac_not_applicable`. |
| Sin actividades | Totales en 0 e indicadores N/A, sin errores. | `test_project_without_activities_has_zero_totals_and_no_indices`: totales en 0, CPI y SPI `null` con NOT_APPLICABLE, EAC y VAC `null`. En el API, `test_create_project_returns_201_location_and_empty_indicators` confirma lo mismo para un proyecto recién creado. La fila 7 vacía del Excel no prueba este caso: solo muestra que una fila sin datos no rompe los totales. |
| Avance real = 0 con AC > 0 | EV = 0, CV = −AC, CPI = 0. EAC = BAC/0 no está definido, así que debe ser N/A y no un error ni infinito. | `test_zero_earned_value_with_cost_is_a_real_zero_cpi_over_budget` (BAC 1.000, PV 500, EV 0, AC 300): CPI = 0 con OVER_BUDGET, CV = −300, EAC y VAC `null`. Coincide con lo esperado. No está en el dataset del demo. |
| Actividad sin iniciar (PV = 0, EV = 0, AC = 0) | CV = SV = 0. CPI y SPI N/A. EAC, ETC y VAC N/A. | `test_zero_planned_value_without_progress_makes_spi_not_applicable` y `test_zero_actual_cost_without_progress_makes_cpi_eac_and_vac_not_applicable`: CPI y SPI `null` con NOT_APPLICABLE, EAC y VAC `null`. El API no calcula ETC; ese valor solo está en el Excel. |

**Prueba de punta a punta (prompt #27):** además de las pruebas unitarias, creé un proyecto temporal con una actividad por caso y revisé la respuesta del API y lo que muestra el front. Todo coincidió con lo esperado:

| Caso (BAC 1.000) | Resultado en el API y en la pantalla |
|---|---|
| AC = 0 con avance (50 % plan, 40 % real) | CPI, EAC y VAC no aplican; SPI 0,8000 atrasado |
| Avance real 0 con AC 300 | CPI 0,0000 sobre presupuesto; EAC y VAC no aplican |
| 0 % planificado con avance (10 % real, AC 100) | SPI no aplica; CPI 1,0000 en presupuesto; EAC 1.000 |
| Sin iniciar (todo en 0) | CPI, SPI, EAC y VAC no aplican; CV y SV en 0 |
| Exactamente según plan (40 % / 40 %, AC 400) | CPI 1,0000 en presupuesto y SPI 1,0000 a tiempo |
| Terminada al 100 % con AC 900 | CPI 1,1111 bajo presupuesto; EAC 900; VAC 100 |
| Proyecto sin actividades | Montos en 0, índices sin calcular y el mensaje "Aún sin datos suficientes" |

También envié datos inválidos (BAC 0, 101 % planificado, AC negativo, nombre vacío, un BAC con más dígitos de los permitidos y montos con 3 decimales): todos respondieron 422 con el campo que falló, y no se guardó nada. Al terminar borré el proyecto temporal.

**Comparación con el Excel**
- Qué esperaba encontrar y qué encontré: Esperaba coincidencia total, salvo redondeo. En `docs/EVM_demo.xlsx` encontré 36 de 36 métricas comparables en COINCIDE y 0 en DIFERENTE: 32 son valores que devuelve el API y 4 son el ETC, que el API no calcula y que obtuve como EAC − AC con los valores del API. Las 9 PENDIENTE son la fila 7 vacía, que no tiene valor de API porque no hay actividad. (El "40 de 40" del prompt #15 fue un cruce anterior, con `evm_ejercicio_v2.xlsx` cargado con los datos del demo.)
- Las diferencias del primer cruce (0,00333): Solo aparecieron en EAC, ETC y VAC de Desarrollo backend. El Excel da 26.666.666,6667 y la API 26.666.666,67. La causa es que la API redondea a 2 decimales (centavos). Lo encontré mirando que la diferencia era la misma en las tres métricas (EAC y ETC con signo negativo, VAC positivo, porque VAC = BAC − EAC) y que 0,00333 cae dentro del error máximo de redondear a 2 decimales (0,005). Los CPI y SPI tienen diferencias de ~1e-5 por la misma razón, con 4 decimales.


## 6. Una decisión de arquitectura que tomé por mi cuenta

- **Cuál fue y cuándo la tomé:** decidí que los indicadores EVM (PV, EV, CV, SV, CPI, SPI, EAC, VAC) se calculan al leer y nunca se guardan en la base de datos, con la lógica EVM como funciones puras sin dependencias de FastAPI ni SQLAlchemy. La tomé antes de pedirle el plan a la IA: está en mi prompt #5, en la lista "Decisiones que ya tomé". La IA la cuestionó por incompleta (faltaban `Decimal` y redondeo solo al presentar), pero no la cambió.
- **Alternativas que consideré y por qué las descarté** (las dos quedaron registradas en `docs/PLAN.md`, D4 y §2):
  - Guardar `pv`, `ev`, `cpi`... como columnas y actualizarlas al guardar: duplica datos derivados y pueden quedar desactualizados si alguien edita una fila por fuera del API.
  - Calcular en el frontend: obliga a mantener las fórmulas en dos lenguajes, con dos fuentes de verdad que pueden divergir.
- **Cómo se refleja en el código:** la tabla `activities` solo guarda los datos de entrada (BAC, % planificado, % real y AC) y no tiene columnas derivadas (`db/init/01_schema.sql`). El cálculo vive en `backend/app/domain/evm/`, los servicios lo invocan al leer y los routers no tienen lógica. El dominio se prueba sin base de datos (54 pruebas unitarias, 100 % de cobertura del dominio). El frontend solo muestra lo que entrega el API.
- **Qué me permitió hacer después que de otro modo habría sido difícil:**
  - Consolidar el proyecto con la misma función que calcula una actividad, aplicada a las sumas, sin duplicar fórmulas (prompt #8, regla 5).
  - Decidir el estado con el valor sin redondear, como en el caso CPI 0,99996 que se muestra "1.0000" pero es `OVER_BUDGET`.
  - Comparar el API contra mi Excel con el mismo dataset (36 de 36 coincidencias en `docs/EVM_demo.xlsx`, sección 5).
  - Cambiar una fórmula sin migrar datos.
- **En qué escenario la cambiaría:** si necesitara historial por fecha de corte, como una curva S o la evolución del CPI, tendría que guardar instantáneas por corte. También si el listado de proyectos creciera tanto que recalcular en cada lectura costara demasiado, usaría una vista materializada o caché. En ambos casos las instantáneas serían un registro aparte y la función pura seguiría siendo la única fuente de las fórmulas.

**Evidencia:** prompt #5 en `docs/prompts-log.md`; `docs/PLAN.md` §1 (D3 y D4); `db/init/01_schema.sql`; `backend/app/domain/evm/`.

---

## 7. Reflexión honesta: qué haría diferente

- **Qué me consumió más tiempo del que debía y por qué:** `Entender lo que tenia que hacer, puesto que nunca lo habia realizado ni tocado como tal tenia que entenderlo bien para saber que tenia que hacer con la ia y como validarlo.`
- **Dónde la IA me hizo avanzar más rápido, y dónde me hizo perder tiempo o me llevó por mal camino:** `me hizo avanzar muy rapido en todo lo que es codigo y pruebas, sin embargo me llevo por mal camino al momento de respetar las reglas y hacer commits en mi nombre sin cambiar de rama en loop para terminar el proyecto rapido.`
- **Qué delegué y, mirando atrás, debí entender o hacer yo primero:** `delegue las pruebas unitarias y la nueva visual del front para que se viera mejor y debi hacerlo yo primero para no perder trabajo ni tokens sino tener esa visual de una vez. `
- **Cómo manejé Git, las ramas apiladas y los PR pendientes, y qué haría distinto:** `No lo manejé bien. Cada rama feature la creé encima de la anterior y no desde develop, así que quedaron apiladas (scaffolding → motor → API → dashboard → visualización). No abrí los PR a medida que terminaba cada feature: develop y main se quedaron en el commit inicial hasta el cierre, y los PR los abrí todos al final, en orden. Además tuve problemas con GitHub Desktop al hacer los commits (prompt #9) y en una iteración anterior la IA hizo commits en la rama equivocada, por eso decidí hacer yo los commits. Si lo repitiera, al terminar cada feature abriría su PR, lo integraría a develop y crearía la siguiente rama desde develop actualizado, y usaría siempre la misma herramienta (git por consola) para no mezclar flujos.`
- **Qué parte del resultado no me deja satisfecho y qué haría con un día más:** `optimizaria el front, revisaria el funcionamiento y como se manejo la db puesto que aunque se reviso la creación y todo debido al tiempo gastaba mas tiempo en entender y asegurar que se hiciera bien en lugar de que fuera escalable.`
- **Si mañana empezara otra tarea en un dominio desconocido, qué cambiaría en mi forma de trabajar con IA:** `lo primero seria revisar las reglas,skills entre otras en este caso como era mi herramienta de trabajo no las revise al 100 % y eso pudo generar errores, lo segundo seria acudir con un experto en el tema para no consumir tanto tiempo entendiendo el problema y de igual manera depender de las IA para que me explicaran puesto que estas tambien pueden cometer errores. `

---

## 8. Prompts de otra IA

Prompts enviados a herramientas distintas de Claude Code (ChatGPT, Copilot, Claude web y v0), copiados textualmente y
en orden cronológico.

### Prompt externo #1
- **Fecha / hora:** `2026-10-02 11:23`
- **Herramienta:** `ChatGPT, Copilot, Claude`
- **Prompt:** `¿Qué es EVM y para qué sirve en la gestión de proyectos?`
- **Para qué:** `Aprender qué es el EVM y cómo funciona para poder explicarlo.`

- **Qué hizo la IA (una línea):** `Me respondió las preguntas con un ejemplo.`
- **Qué hice yo con eso:** `Tomé notas y estuve practicando para que cuando comenzara la prueba tuviera el conocimiento y las pruebas suficientes para desarrollarlo sin depender de conocimiento de la IA.`

**Respuesta (Copilot):** El **EVM** (Earned Value Management) es una técnica que integra alcance, tiempo y costo para medir desempeño y progreso. Sirve para comparar lo planificado con lo ejecutado y detectar desviaciones.

**Respuesta (Claude):** **EVM** (Gestión del Valor Ganado) mide el desempeño de un proyecto expresando en dinero tres cosas: lo que se planeó hacer (PV), lo que realmente se hizo (EV) y lo que realmente costó (AC). Con ellas responde si el proyecto va adelantado o atrasado, si está gastando más o menos de lo que vale el trabajo hecho y cuánto costará al terminar si sigue igual.

---

### Prompt externo #2
- **Fecha / hora:** `2026-10-02 11:30`
- **Herramienta:** `ChatGPT, Copilot, Claude`
- **Prompt:** `¿Cuáles son las variables principales de EVM y qué significa cada una: BAC, PV, EV y AC?`
- **Para qué:** `Entender las variables y cómo se utilizan.`

- **Qué hizo la IA (una línea):** `Me respondió cada una de las variables con un ejemplo de uso.`
- **Qué hice yo con eso:** `Tomé notas y estuve practicando para que cuando comenzara la prueba tuviera el conocimiento y las pruebas suficientes para desarrollarlo sin depender de conocimiento de la IA.`

**Respuesta (Copilot):**  
- **BAC**: Budget at Completion, presupuesto total aprobado.  
- **PV**: Planned Value, valor planificado según cronograma.  
- **EV**: Earned Value, valor ganado según avance real.  
- **AC**: Actual Cost, costo real incurrido.

**Respuesta (Claude):**  
- **BAC**: presupuesto total aprobado; no cambia con el avance. Ej.: 10.000.  
- **PV**: valor del trabajo que debía estar hecho a la fecha de corte. Ej.: 50 % planificado → 5.000.  
- **EV**: valor del trabajo realmente hecho a la fecha de corte. Ej.: 40 % real → 4.000.  
- **AC**: dinero realmente gastado hasta la fecha de corte. Ej.: 5.000.

---

### Prompt externo #3
- **Fecha / hora:** `2026-10-02 12:15`
- **Herramienta:** `ChatGPT, Copilot, Claude`
- **Prompt:** `¿Cómo se calcula el valor planificado (PV) y qué representa dentro de un proyecto?`
- **Para qué:** `Entender cómo se calcula el valor planificado y cómo se utiliza dentro de EVM.`

- **Qué hizo la IA (una línea):** `Me explicó la fórmula para calcular PV y me mostró algunos ejemplos para entender cómo se relaciona el porcentaje planificado con el presupuesto.`
- **Qué hice yo con eso:** `Tomé notas y realicé algunos ejercicios manualmente para comprobar que entendía cómo obtener el valor planificado.`

**Respuesta (Copilot):** El **PV** se calcula multiplicando el BAC por el porcentaje planificado de avance. Representa cuánto valor debería haberse completado según el plan.

**Respuesta (Claude):** **PV = BAC × % planificado**. Ej.: 10.000 × 50 % = 5.000. Es la línea base del cronograma: el punto contra el que se compara el EV para saber si el proyecto va adelantado o atrasado.

---

### Prompt externo #4
- **Fecha / hora:** `2026-10-02 13:00`
- **Herramienta:** `ChatGPT, Copilot, Claude`
- **Prompt:** `¿Cómo se calcula el valor ganado (EV) y cuál es la diferencia entre el valor ganado y el porcentaje de avance real?`
- **Para qué:** `Entender cómo se obtiene el valor ganado y cómo se relaciona con el avance real de una actividad.`

- **Qué hizo la IA (una línea):** `Me explicó cómo calcular EV utilizando el presupuesto y el porcentaje de avance real, además de diferenciarlo del porcentaje de avance.`
- **Qué hice yo con eso:** `Realicé ejercicios comparando el porcentaje de avance con el valor monetario obtenido para entender mejor la diferencia.`

**Respuesta (Copilot):** El **EV** se obtiene multiplicando el BAC por el porcentaje de avance real. El porcentaje de avance es solo un indicador, mientras que el EV traduce ese avance en valor monetario.

**Respuesta (Claude):** **EV = BAC × % real**. Ej.: 10.000 × 40 % = 4.000. El % real es un dato físico (cuánto se terminó) y el EV es ese mismo avance en dinero. Al estar en dinero, el EV se puede comparar directamente con PV y AC y sumar entre actividades de distinto tamaño.

---

### Prompt externo #5
- **Fecha / hora:** `2026-10-02 13:45`
- **Herramienta:** `ChatGPT, Copilot, Claude`
- **Prompt:** `¿Qué significa el costo real (AC) y cómo se diferencia del presupuesto planificado?`
- **Para qué:** `Entender qué representa el costo real dentro de EVM y cómo se utiliza para comparar el desempeño del proyecto.`

- **Qué hizo la IA (una línea):** `Me explicó que AC representa el costo que realmente se ha gastado y que puede ser diferente al presupuesto o al valor del trabajo realizado.`
- **Qué hice yo con eso:** `Tomé ejemplos y comparé el costo real con el valor ganado para entender cómo identificar si una actividad estaba gastando más o menos de lo esperado.`

**Respuesta (Copilot):** El **AC** es el gasto real incurrido en una actividad. Se diferencia del presupuesto porque refleja lo que efectivamente se ha pagado, no lo que estaba previsto.

**Respuesta (Claude):** **AC** es un dato de entrada: no se calcula, se registra. El BAC y el PV dicen lo que se esperaba gastar; el AC dice lo que realmente se gastó. Para medir eficiencia, el AC se compara con el **EV** (no con el PV). Ej.: EV = 4.000 y AC = 5.000 → se gastaron 5.000 para producir trabajo que vale 4.000.

---

### Prompt externo #6
- **Fecha / hora:** `2026-10-02 14:30`
- **Herramienta:** `ChatGPT, Copilot, Claude`
- **Prompt:** `¿Cómo se calculan CV y SV, y qué significa que sus resultados sean positivos o negativos?`
- **Para qué:** `Entender cómo identificar las variaciones de costo y tiempo dentro de un proyecto.`

- **Qué hizo la IA (una línea):** `Me explicó las fórmulas CV = EV - AC y SV = EV - PV, junto con la interpretación de los resultados positivos, negativos y cero.`
- **Qué hice yo con eso:** `Practiqué diferentes casos manualmente para entender qué significaba cada resultado y cómo saber si una actividad estaba por encima o por debajo de lo esperado.`

**Respuesta (Copilot):**  
- **CV** = EV - AC → variación de costos.  
- **SV** = EV - PV → variación de cronograma.  
Positivo = favorable, negativo = desfavorable, cero = conforme al plan.

**Respuesta (Claude):**  
- **CV = EV − AC**: > 0 por debajo del presupuesto, < 0 sobrecosto, = 0 en presupuesto. Ej.: 4.000 − 5.000 = −1.000 (sobrecosto).  
- **SV = EV − PV**: > 0 adelantado, < 0 atrasado, = 0 a tiempo. Ej.: 4.000 − 5.000 = −1.000 (atrasado).  
Ambas se expresan en dinero, no en días.

---

### Prompt externo #7
- **Fecha / hora:** `2026-10-02 15:15`
- **Herramienta:** `ChatGPT, Copilot, Claude`
- **Prompt:** `¿Qué son CPI y SPI, cómo se calculan y cómo puedo interpretar sus resultados para saber si un proyecto va bien?`
- **Para qué:** `Entender los indicadores de desempeño de costos y cronograma y aprender a interpretar sus resultados.`

- **Qué hizo la IA (una línea):** `Me explicó las fórmulas CPI = EV / AC y SPI = EV / PV y cómo interpretar valores mayores, menores o iguales a 1.`
- **Qué hice yo con eso:** `Realicé varios ejercicios y comprobé manualmente que la interpretación de los índices coincidiera con los valores de EV, AC y PV.`

**Respuesta (Copilot):**  
- **CPI** = EV / AC → eficiencia de costos.  
- **SPI** = EV / PV → eficiencia de cronograma.  
>1 = eficiente, <1 = ineficiente, =1 = conforme al plan.

**Respuesta (Claude):**  
- **CPI = EV / AC**: cuánto valor se produce por cada peso gastado. Ej.: 4.000 / 5.000 = 0,80 (por cada peso gastado se producen 0,80 de valor).  
- **SPI = EV / PV**: qué fracción del avance planificado se logró. Ej.: 4.000 / 5.000 = 0,80 (se avanzó al 80 % del ritmo planeado).  
> 1 favorable, < 1 desfavorable, = 1 según plan. Ojo: si AC o PV valen 0, la división no está definida y debe manejarse aparte.

---

### Prompt externo #8
- **Fecha / hora:** `2026-10-02 16:00`
- **Herramienta:** `ChatGPT, Copilot, Claude`
- **Prompt:** `¿Cómo se calcula el costo estimado al finalizar (EAC) y la variación al finalizar (VAC), y qué me dicen sobre el presupuesto futuro?`
- **Para qué:** `Entender cómo estimar el costo final de un proyecto y cómo saber si se espera terminar por encima o por debajo del presupuesto.`

- **Qué hizo la IA (una línea):** `Me explicó las fórmulas EAC = BAC / CPI y VAC = BAC - EAC y cómo interpretar los resultados.`
- **Qué hice yo con eso:** `Realicé ejercicios con diferentes valores de CPI y comprobé cómo estos afectaban el costo estimado al finalizar.`

**Respuesta (Copilot):**  
- **EAC** = BAC / CPI → costo estimado al final.  
- **VAC** = BAC - EAC → diferencia entre presupuesto y costo final esperado.

**Respuesta (Claude):**  
- **EAC = BAC / CPI**: costo final proyectado si la eficiencia actual se mantiene. Ej.: 10.000 / 0,80 = 12.500.  
- **VAC = BAC − EAC**: > 0 se espera terminar bajo presupuesto, < 0 se espera sobrecosto. Ej.: 10.000 − 12.500 = −2.500.  
Esta fórmula supone que el CPI actual se mantiene hasta el final; si CPI = 0, el EAC no se puede calcular.

---

### Prompt externo #9
- **Fecha / hora:** `2026-10-02 16:45`
- **Herramienta:** `ChatGPT, Copilot, Claude`
- **Prompt:** `¿Cómo se calculan los indicadores EVM de un proyecto completo cuando tiene varias actividades con presupuestos y avances diferentes?`
- **Para qué:** `Entender cómo consolidar los resultados de diferentes actividades para obtener los indicadores generales del proyecto.`

- **Qué hizo la IA (una línea):** `Me explicó que primero se deben consolidar los valores de BAC, PV, EV y AC de las actividades y posteriormente calcular los indicadores generales.`
- **Qué hice yo con eso:** `Hice un ejemplo con varias actividades y realicé los cálculos manualmente para comprobar que entendía cómo pasar de los datos individuales al resultado consolidado.`

**Respuesta (Copilot):** Para calcular los indicadores de un proyecto completo, primero se suman los valores de **BAC**, **PV**, **EV** y **AC** de todas las actividades. Luego, con esos valores consolidados, se aplican las fórmulas de CV, SV, CPI, SPI, EAC y VAC como si fueran un único proyecto. Esto permite evaluar el desempeño global y no solo el de actividades individuales.

**Respuesta (Claude):** Se suman **BAC, PV, EV y AC** de todas las actividades y con esos totales se aplican las fórmulas. Error común: **no** se deben promediar los CPI o SPI de cada actividad. El correcto es CPI total = ΣEV / ΣAC, que pondera automáticamente cada actividad según su peso en dinero. Ej.: A (EV 4.000, AC 5.000) + B (EV 1.000, AC 500) → CPI = 5.000 / 5.500 ≈ 0,91, no el promedio (0,8 + 2,0) / 2 = 1,4.

---

### Prompt externo #10
- **Fecha / hora:** `2026-10-02 17:30`
- **Herramienta:** `ChatGPT, Copilot, Claude`
- **Prompt:** `¿Cómo puedo comprobar manualmente que las fórmulas de EVM están bien aplicadas y que los resultados tienen sentido antes de programarlas?`
- **Para qué:** `Validar que realmente entendía las fórmulas antes de comenzar a implementarlas en el proyecto.`

- **Qué hizo la IA (una línea):** `Me recomendó realizar cálculos manuales con diferentes escenarios y comprobar que los resultados fueran coherentes con la situación del proyecto.`
- **Qué hice yo con eso:** `Realicé una última prueba manual con valores de BAC, porcentaje planificado, porcentaje real y AC, comparé los resultados de PV, EV, CV, SV, CPI, SPI, EAC y VAC y confirmé que las fórmulas tenían sentido antes de comenzar a programarlas.`

**Respuesta (Copilot):** Para comprobar manualmente las fórmulas de **EVM**, se recomienda crear escenarios simples con valores de BAC, porcentaje planificado, porcentaje real y AC. Luego calcular PV, EV, CV, SV, CPI, SPI, EAC y VAC y verificar que los resultados sean coherentes:  
- Si el avance real es menor al planificado, EV < PV.  
- Si el costo real supera al valor ganado, AC > EV y el CV será negativo.  
- Si CPI < 1, el proyecto está gastando más de lo previsto.  
Este chequeo asegura que las fórmulas están bien aplicadas antes de programarlas.

**Respuesta (Claude):** Arma un caso completo y comprueba que los signos sean coherentes entre sí. Ej.: BAC 10.000, 50 % planificado, 40 % real, AC 5.000 → PV 5.000, EV 4.000, CV −1.000, SV −1.000, CPI 0,80, SPI 0,80, EAC 12.500, VAC −2.500. Revisa que:  
- CV < 0 ⇔ CPI < 1 ⇔ VAC < 0 (deben coincidir siempre).  
- SV < 0 ⇔ SPI < 1.  
- Si % real = % planificado y AC = EV, todo da 0 o 1 (caso "según plan").  
Prueba también casos borde: AC = 0, PV = 0 (0 % planificado) y 100 % de avance. Esos mismos casos sirven después como pruebas unitarias del código.



---

### Prompt externo #11
- **Fecha / hora:** `2026-10-02 17:30`
- **Herramienta:** `v0`
- **Prompt:** `generame un front profesional para mostrar un EVM `
- **Para qué:** `mejorar visualmente el proyecto puesto que al no darle a la IA un esqueleto no se realizo de manera correcta. `

- **Qué hizo la IA (una línea):** `me genero una visual completa de un EVM el cual use como guia para mejorar la visual del proyecto.`
- **Qué hice yo con eso:** `revise con ayuda de la IA que cosas podia tomar para el proyecto sin romperlo y como podian afectar positivamente el proyecto.`