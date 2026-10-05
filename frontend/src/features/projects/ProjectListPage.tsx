import { Plus } from 'lucide-react';
import { useState } from 'react';
import { Link, useNavigate } from 'react-router';
import { useProjects } from '../../api/queries';
import { ErrorMessage, LoadingMessage } from '../../components/Feedback';
import { Modal } from '../../components/Modal';
import { PageLayout } from '../../components/PageLayout';
import { CpiBadge, SpiBadge } from '../../components/StatusBadge';
import { formatDate, formatMoney } from '../../lib/format';
import { readOverallTone } from '../../lib/narrative';
import { PROJECTS_LABEL, projectPath } from '../../lib/routes';
import { ProjectForm } from './ProjectForm';

export function ProjectListPage() {
  const projects = useProjects();
  const navigate = useNavigate();
  const [isCreating, setIsCreating] = useState(false);

  return (
    <PageLayout crumbs={[{ label: PROJECTS_LABEL }]}>
      <header className="hero">
        <div>
          <p className="eyebrow">Valor ganado</p>
          <h1>{PROJECTS_LABEL}</h1>
          <p>
            Estado de costo (CPI) y cronograma (SPI) de cada proyecto, consolidado de sus
            actividades.
          </p>
        </div>
        <div className="hero-actions">
          <button type="button" className="button-primary" onClick={() => setIsCreating(true)}>
            <Plus aria-hidden="true" />
            Nuevo proyecto
          </button>
        </div>
      </header>

      <section className="card table-card" aria-labelledby="projects-title">
        <header className="card-heading">
          <div>
            <h2 id="projects-title">Portafolio</h2>
            <p>Abre un proyecto para ver y editar sus actividades</p>
          </div>
        </header>
        {projects.isPending && <LoadingMessage text="Cargando proyectos…" />}
        {projects.isError && <ErrorMessage error={projects.error} />}
        {projects.isSuccess && projects.data.length === 0 && (
          <p className="empty-state">Todavía no hay proyectos. Crea el primero.</p>
        )}
        {projects.isSuccess && projects.data.length > 0 && (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th scope="col">Proyecto</th>
                  <th scope="col">Fecha de corte</th>
                  <th scope="col" className="numeric">
                    Actividades
                  </th>
                  <th scope="col" className="numeric">
                    Presupuesto (BAC)
                  </th>
                  <th scope="col">Costo (CPI)</th>
                  <th scope="col">Cronograma (SPI)</th>
                  <th scope="col" className="numeric">
                    Estimado final (EAC)
                  </th>
                </tr>
              </thead>
              <tbody>
                {projects.data.map((project) => (
                  <tr key={project.id}>
                    <th scope="row">
                      <span className="row-name">
                        <span
                          className={`row-dot tone-${readOverallTone(project.indicators)}`}
                          aria-hidden="true"
                        />
                        <Link to={projectPath(project.id)}>{project.name}</Link>
                      </span>
                      {project.description && (
                        <small className="row-description">{project.description}</small>
                      )}
                    </th>
                    <td>{formatDate(project.cutoff_date)}</td>
                    <td className="numeric">{project.activity_count}</td>
                    <td className="numeric">{formatMoney(project.indicators.bac)}</td>
                    <td>
                      <CpiBadge index={project.indicators.cpi} />
                    </td>
                    <td>
                      <SpiBadge index={project.indicators.spi} />
                    </td>
                    <td className="numeric">{formatMoney(project.indicators.eac)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <Modal title="Nuevo proyecto" open={isCreating} onClose={() => setIsCreating(false)}>
        <ProjectForm
          onCancel={() => setIsCreating(false)}
          onSaved={(project) => navigate(projectPath(project.id))}
        />
      </Modal>
    </PageLayout>
  );
}
