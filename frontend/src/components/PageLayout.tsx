import { Activity, CalendarDays } from 'lucide-react';
import { Fragment, type ReactNode } from 'react';
import { Link } from 'react-router';
import { formatDate } from '../lib/format';
import { PROJECTS_PATH } from '../lib/routes';

export interface Crumb {
  label: string;
  to?: string;
}

interface PageLayoutProps {
  crumbs: Crumb[];
  cutoffDate?: string | null;
  children: ReactNode;
}

const CRUMB_SEPARATOR = '/';

/** Top bar with the breadcrumbs and the cutoff date, followed by the page content. */
export function PageLayout({ crumbs, cutoffDate, children }: PageLayoutProps) {
  return (
    <>
      <header className="topbar">
        <Link to={PROJECTS_PATH} className="topbar-brand" aria-label="EVM Tracker, ir a proyectos">
          <Activity aria-hidden="true" />
        </Link>
        <nav className="breadcrumbs" aria-label="Ruta">
          {crumbs.map((crumb, position) => (
            <Fragment key={crumb.label}>
              {position > 0 && <span aria-hidden="true">{CRUMB_SEPARATOR}</span>}
              {crumb.to === undefined ? (
                <strong aria-current="page">{crumb.label}</strong>
              ) : (
                <Link to={crumb.to}>{crumb.label}</Link>
              )}
            </Fragment>
          ))}
        </nav>
        {cutoffDate !== undefined && (
          <p className="topbar-date">
            <CalendarDays aria-hidden="true" />
            Corte: <strong>{formatDate(cutoffDate)}</strong>
          </p>
        )}
      </header>
      <div className="content-wrap">{children}</div>
    </>
  );
}
