import { BrowserRouter, Route, Routes } from 'react-router';
import { PageLayout } from './components/PageLayout';
import { Sidebar } from './components/Sidebar';
import { ProjectDetailPage } from './features/projects/ProjectDetailPage';
import { ProjectListPage } from './features/projects/ProjectListPage';
import { PROJECTS_LABEL, PROJECTS_PATH, PROJECT_DETAIL_ROUTE } from './lib/routes';

function NotFoundPage() {
  return (
    <PageLayout crumbs={[{ label: PROJECTS_LABEL, to: PROJECTS_PATH }, { label: 'No encontrada' }]}>
      <p className="empty-state">Página no encontrada.</p>
    </PageLayout>
  );
}

export function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path={PROJECTS_PATH} element={<ProjectListPage />} />
            <Route path={PROJECT_DETAIL_ROUTE} element={<ProjectDetailPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
