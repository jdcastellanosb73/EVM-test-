-- EVM Tracker schema. Single source of truth for the database structure:
-- loaded by the db service on first start and by db-test for integration tests.

CREATE TABLE projects (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name         VARCHAR(120) NOT NULL,
    description  VARCHAR(500),
    cutoff_date  DATE,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_projects_name UNIQUE (name),
    CONSTRAINT ck_projects_name_not_blank CHECK (length(trim(name)) > 0)
);

CREATE TABLE activities (
    id                    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    project_id            BIGINT NOT NULL,
    name                  VARCHAR(120) NOT NULL,
    budget_at_completion  NUMERIC(15, 2) NOT NULL,
    planned_percent       NUMERIC(5, 2) NOT NULL,
    actual_percent        NUMERIC(5, 2) NOT NULL,
    actual_cost           NUMERIC(15, 2) NOT NULL,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_activities_project
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
    CONSTRAINT uq_activities_project_name UNIQUE (project_id, name),
    CONSTRAINT ck_activities_name_not_blank CHECK (length(trim(name)) > 0),
    CONSTRAINT ck_activities_bac_positive CHECK (budget_at_completion > 0),
    CONSTRAINT ck_activities_planned_percent_range CHECK (planned_percent BETWEEN 0 AND 100),
    CONSTRAINT ck_activities_actual_percent_range CHECK (actual_percent BETWEEN 0 AND 100),
    CONSTRAINT ck_activities_actual_cost_non_negative CHECK (actual_cost >= 0)
);

CREATE INDEX ix_activities_project_id ON activities (project_id);

CREATE FUNCTION set_updated_at() RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_projects_updated_at
    BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_activities_updated_at
    BEFORE UPDATE ON activities
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
