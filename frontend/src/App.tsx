import { BrowserRouter, Link, Route, Routes } from 'react-router';
import { ProjectDetailPage } from './features/projects/ProjectDetailPage';
import { ProjectListPage } from './features/projects/ProjectListPage';

export function App() {
  return (
    <BrowserRouter>
      <header className="app-header">
        <Link to="/" className="app-title">
          EVM Tracker
        </Link>
        <span className="app-tagline">Valor Ganado por proyecto</span>
      </header>
      <main className="app">
        <Routes>
          <Route path="/" element={<ProjectListPage />} />
          <Route path="/projects/:projectId" element={<ProjectDetailPage />} />
          <Route path="*" element={<p className="empty-state">Página no encontrada.</p>} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
