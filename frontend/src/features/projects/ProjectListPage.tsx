import { useState } from 'react';
import { Link, useNavigate } from 'react-router';
import { useProjects } from '../../api/queries';
import { ErrorMessage, LoadingMessage } from '../../components/Feedback';
import { Modal } from '../../components/Modal';
import { CpiBadge, SpiBadge } from '../../components/StatusBadge';
import { formatDate, formatMoney } from '../../lib/format';
import { ProjectForm } from './ProjectForm';

export function ProjectListPage() {
  const projects = useProjects();
  const navigate = useNavigate();
  const [isCreating, setIsCreating] = useState(false);

  return (
    <section>
      <header className="page-header">
        <div>
          <h1>Proyectos</h1>
          <p className="page-subtitle">
            Estado de costo (CPI) y cronograma (SPI) de cada proyecto, consolidado de sus
            actividades.
          </p>
        </div>
        <button type="button" className="button-primary" onClick={() => setIsCreating(true)}>
          Nuevo proyecto
        </button>
      </header>

      {projects.isPending && <LoadingMessage text="Cargando proyectos…" />}
      {projects.isError && <ErrorMessage error={projects.error} />}
      {projects.isSuccess && projects.data.length === 0 && (
        <p className="empty-state">Todavía no hay proyectos. Crea el primero.</p>
      )}
      {projects.isSuccess && projects.data.length > 0 && (
        <div className="table-scroll">
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
                    <Link to={`/projects/${project.id}`}>{project.name}</Link>
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

      <Modal title="Nuevo proyecto" open={isCreating} onClose={() => setIsCreating(false)}>
        <ProjectForm
          onCancel={() => setIsCreating(false)}
          onSaved={(project) => navigate(`/projects/${project.id}`)}
        />
      </Modal>
    </section>
  );
}
