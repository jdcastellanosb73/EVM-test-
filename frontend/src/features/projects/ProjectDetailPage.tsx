import { useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router';
import { useDeleteActivity, useDeleteProject, useProject } from '../../api/queries';
import type { Activity, Project } from '../../api/types';
import { ErrorMessage, LoadingMessage } from '../../components/Feedback';
import { Modal } from '../../components/Modal';
import { formatDate } from '../../lib/format';
import { ActivityForm } from '../activities/ActivityForm';
import { ActivityTable } from '../activities/ActivityTable';
import { ProjectForm } from './ProjectForm';
import { ProjectIndicators } from './ProjectIndicators';

type ActivityEditor =
  { mode: 'closed' } | { mode: 'create' } | { mode: 'edit'; activity: Activity };

const CLOSED: ActivityEditor = { mode: 'closed' };

export function ProjectDetailPage() {
  const projectId = Number(useParams().projectId);
  if (!Number.isInteger(projectId) || projectId <= 0) {
    return <p className="empty-state">El proyecto solicitado no existe.</p>;
  }
  return <ProjectDetail projectId={projectId} />;
}

function ProjectDetail({ projectId }: { projectId: number }) {
  const project = useProject(projectId);

  return (
    <section>
      <Link to="/" className="back-link">
        ← Proyectos
      </Link>
      {project.isPending && <LoadingMessage text="Cargando proyecto…" />}
      {project.isError && <ErrorMessage error={project.error} />}
      {project.isSuccess && <ProjectView project={project.data} />}
    </section>
  );
}

function ProjectView({ project }: { project: Project }) {
  const navigate = useNavigate();
  const [isEditingProject, setIsEditingProject] = useState(false);
  const [activityEditor, setActivityEditor] = useState<ActivityEditor>(CLOSED);
  const deleteProject = useDeleteProject();
  const deleteActivity = useDeleteActivity(project.id);

  const closeActivityEditor = () => setActivityEditor(CLOSED);

  const confirmDeleteProject = () => {
    const message = `¿Eliminar "${project.name}" y sus ${project.activities.length} actividades?`;
    if (window.confirm(message)) {
      deleteProject.mutate(project.id, { onSuccess: () => navigate('/') });
    }
  };

  const confirmDeleteActivity = (activity: Activity) => {
    if (window.confirm(`¿Eliminar la actividad "${activity.name}"?`)) {
      deleteActivity.mutate(activity.id);
    }
  };

  return (
    <>
      <header className="page-header">
        <div>
          <h1>{project.name}</h1>
          <p className="page-subtitle">
            Fecha de corte: {formatDate(project.cutoff_date)}
            {project.description && ` · ${project.description}`}
          </p>
        </div>
        <div className="header-actions">
          <button
            type="button"
            className="button-secondary"
            onClick={() => setIsEditingProject(true)}
          >
            Editar proyecto
          </button>
          <button
            type="button"
            className="button-secondary danger"
            disabled={deleteProject.isPending}
            onClick={confirmDeleteProject}
          >
            Eliminar proyecto
          </button>
        </div>
      </header>

      {deleteProject.isError && <ErrorMessage error={deleteProject.error} />}
      <ProjectIndicators indicators={project.indicators} />

      <section className="panel" aria-labelledby="activities-title">
        <div className="panel-header">
          <h2 id="activities-title">Actividades</h2>
          <button
            type="button"
            className="button-primary"
            onClick={() => setActivityEditor({ mode: 'create' })}
          >
            Nueva actividad
          </button>
        </div>
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
