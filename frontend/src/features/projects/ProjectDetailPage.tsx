import { Pencil, Plus, Trash2 } from 'lucide-react';
import { Suspense, lazy, useState } from 'react';
import { useNavigate, useParams } from 'react-router';
import { useDeleteActivity, useDeleteProject, useProject } from '../../api/queries';
import type { Activity, Project } from '../../api/types';
import { ErrorMessage, LoadingMessage } from '../../components/Feedback';
import { Modal } from '../../components/Modal';
import { PageLayout, type Crumb } from '../../components/PageLayout';
import { ActivityForm } from '../activities/ActivityForm';
import { ActivityTable } from '../activities/ActivityTable';
import { PROJECTS_LABEL, PROJECTS_PATH } from '../../lib/routes';
import { ProjectBanner } from './ProjectBanner';
import { ProjectForm } from './ProjectForm';
import { ProjectHealth } from './ProjectHealth';
import { ProjectIndicators } from './ProjectIndicators';

/** Recharts is heavy: load the chart only when a project detail is shown. */
const EvmChart = lazy(() => import('./EvmChart').then((module) => ({ default: module.EvmChart })));

type ActivityEditor =
  { mode: 'closed' } | { mode: 'create' } | { mode: 'edit'; activity: Activity };

const CLOSED: ActivityEditor = { mode: 'closed' };
const PROJECTS_CRUMB: Crumb = { label: PROJECTS_LABEL, to: PROJECTS_PATH };
const DEFAULT_DESCRIPTION = 'Indicadores de Valor Ganado a la fecha de corte.';

export function ProjectDetailPage() {
  const projectId = Number(useParams().projectId);
  if (!Number.isInteger(projectId) || projectId <= 0) {
    return (
      <PageLayout crumbs={[PROJECTS_CRUMB, { label: 'No encontrado' }]}>
        <p className="empty-state">El proyecto solicitado no existe.</p>
      </PageLayout>
    );
  }
  return <ProjectDetail projectId={projectId} />;
}

function ProjectDetail({ projectId }: { projectId: number }) {
  const project = useProject(projectId);

  if (!project.isSuccess) {
    return (
      <PageLayout crumbs={[PROJECTS_CRUMB, { label: 'Proyecto' }]}>
        {project.isPending && <LoadingMessage text="Cargando proyecto…" />}
        {project.isError && <ErrorMessage error={project.error} />}
      </PageLayout>
    );
  }
  return (
    <PageLayout
      crumbs={[PROJECTS_CRUMB, { label: project.data.name }]}
      cutoffDate={project.data.cutoff_date}
    >
      <ProjectView project={project.data} />
    </PageLayout>
  );
}

function ProjectView({ project }: { project: Project }) {
  const navigate = useNavigate();
  const [isEditingProject, setIsEditingProject] = useState(false);
  const [activityEditor, setActivityEditor] = useState<ActivityEditor>(CLOSED);
  const deleteProject = useDeleteProject();
  const deleteActivity = useDeleteActivity(project.id);

  const openNewActivity = () => setActivityEditor({ mode: 'create' });
  const closeActivityEditor = () => setActivityEditor(CLOSED);

  const confirmDeleteProject = () => {
    const message = `¿Eliminar "${project.name}" y sus ${project.activities.length} actividades?`;
    if (window.confirm(message)) {
      deleteProject.mutate(project.id, { onSuccess: () => navigate(PROJECTS_PATH) });
    }
  };

  const confirmDeleteActivity = (activity: Activity) => {
    if (window.confirm(`¿Eliminar la actividad "${activity.name}"?`)) {
      deleteActivity.mutate(activity.id);
    }
  };

  return (
    <>
      <header className="hero">
        <div>
          <p className="eyebrow">Proyecto</p>
          <h1>{project.name}</h1>
          <p>{project.description ?? DEFAULT_DESCRIPTION}</p>
        </div>
        <div className="hero-actions">
          <button
            type="button"
            className="button-secondary"
            onClick={() => setIsEditingProject(true)}
          >
            <Pencil aria-hidden="true" />
            Editar proyecto
          </button>
          <button
            type="button"
            className="button-secondary danger"
            disabled={deleteProject.isPending}
            onClick={confirmDeleteProject}
          >
            <Trash2 aria-hidden="true" />
            Eliminar proyecto
          </button>
          <button type="button" className="button-primary" onClick={openNewActivity}>
            <Plus aria-hidden="true" />
            Nueva actividad
          </button>
        </div>
      </header>

      {deleteProject.isError && <ErrorMessage error={deleteProject.error} />}
      <ProjectBanner project={project} />
      <ProjectIndicators indicators={project.indicators} />

      <div className="analysis-grid">
        {project.activities.length > 0 ? (
          <Suspense fallback={<LoadingMessage text="Cargando gráfica…" />}>
            <EvmChart activities={project.activities} />
          </Suspense>
        ) : (
          <section className="card chart-card">
            <p className="empty-state">Agrega actividades para ver la gráfica PV / EV / AC.</p>
          </section>
        )}
        <ProjectHealth indicators={project.indicators} />
      </div>

      <section className="card activities-card" aria-labelledby="activities-title">
        <header className="card-heading">
          <div>
            <h2 id="activities-title">Actividades del proyecto</h2>
            <p>Avance, costo e indicadores de cada actividad, con el total del proyecto</p>
          </div>
          <button type="button" className="button-primary" onClick={openNewActivity}>
            <Plus aria-hidden="true" />
            Agregar actividad
          </button>
        </header>
        {deleteActivity.isError && <ErrorMessage error={deleteActivity.error} />}
        {project.activities.length === 0 ? (
          <p className="empty-state">
            Este proyecto no tiene actividades. Agrega una para ver su análisis.
          </p>
        ) : (
          <ActivityTable
            activities={project.activities}
            projectIndicators={project.indicators}
            onEdit={(activity) => setActivityEditor({ mode: 'edit', activity })}
            onDelete={confirmDeleteActivity}
            isDeleting={deleteActivity.isPending}
          />
        )}
      </section>

      <Modal
        title="Editar proyecto"
        open={isEditingProject}
        onClose={() => setIsEditingProject(false)}
      >
        <ProjectForm
          project={project}
          onCancel={() => setIsEditingProject(false)}
          onSaved={() => setIsEditingProject(false)}
        />
      </Modal>

      <Modal
        title={activityEditor.mode === 'edit' ? 'Editar actividad' : 'Nueva actividad'}
        open={activityEditor.mode !== 'closed'}
        onClose={closeActivityEditor}
      >
        <ActivityForm
          projectId={project.id}
          {...(activityEditor.mode === 'edit' && { activity: activityEditor.activity })}
          onCancel={closeActivityEditor}
          onSaved={closeActivityEditor}
        />
      </Modal>
    </>
  );
}
