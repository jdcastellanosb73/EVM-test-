import { Activity, FolderKanban } from 'lucide-react';
import { Link } from 'react-router';
import { PROJECTS_LABEL, PROJECTS_PATH } from '../lib/routes';

/** Every screen of the app belongs to the project portfolio, so "Proyectos" is always active. */
export function Sidebar() {
  return (
    <aside className="sidebar">
      <Link to={PROJECTS_PATH} className="brand">
        <span className="brand-mark">
          <Activity aria-hidden="true" />
        </span>
        <span>
          <strong>EVM Tracker</strong>
          <span>Valor ganado</span>
        </span>
      </Link>
      <nav className="side-nav" aria-label="Navegación principal">
        <Link to={PROJECTS_PATH} className="side-nav__item is-active" aria-current="page">
          <FolderKanban aria-hidden="true" />
          {PROJECTS_LABEL}
        </Link>
      </nav>
    </aside>
  );
}
