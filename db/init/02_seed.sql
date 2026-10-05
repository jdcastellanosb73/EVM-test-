-- Demo data. Loaded only by the db service (never by db-test).

WITH demo_project AS (
    INSERT INTO projects (name, description, cutoff_date)
    VALUES ('Portal de clientes', 'Proyecto de demostración para el análisis de Valor Ganado', DATE '2026-10-03')
    RETURNING id
)
INSERT INTO activities (project_id, name, budget_at_completion, planned_percent, actual_percent, actual_cost)
SELECT demo_project.id, seed.name, seed.budget_at_completion, seed.planned_percent, seed.actual_percent, seed.actual_cost
FROM demo_project
CROSS JOIN (
    VALUES
        ('Diseño UX',           8000000.00, 100.00, 100.00,  7200000.00),
        ('Desarrollo backend', 20000000.00,  60.00,  45.00, 12000000.00),
        ('Pruebas QA',          6000000.00,  20.00,   0.00,        0.00)
) AS seed (name, budget_at_completion, planned_percent, actual_percent, actual_cost);
