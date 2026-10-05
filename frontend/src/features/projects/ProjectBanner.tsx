import { Activity } from 'lucide-react';
import type { Project } from '../../api/types';
import { formatDate, formatMoney } from '../../lib/format';
import { readOverallTone, readProjectVerdict } from '../../lib/narrative';

/** The verdict at a glance, with the budget and the cost spent so far. */
export function ProjectBanner({ project }: { project: Project }) {
  const { indicators } = project;
  return (
    <section className="project-banner" aria-label="Estado del proyecto">
      <span className={`project-icon tone-${readOverallTone(indicators)}`}>
        <Activity aria-hidden="true" />
      </span>
      <div className="project-details">
        <span>Estado a la fecha de corte</span>
        <strong>{readProjectVerdict(indicators)}</strong>
        <small>
          {project.activities.length} actividades
          <i aria-hidden="true" />
          Corte {formatDate(project.cutoff_date)}
        </small>
      </div>
      <dl className="project-meta">
        <div>
          <dt>Presupuesto total (BAC)</dt>
          <dd>{formatMoney(indicators.bac)}</dd>
        </div>
        <div>
          <dt>Costo real (AC)</dt>
          <dd>{formatMoney(indicators.ac)}</dd>
        </div>
      </dl>
    </section>
  );
}
