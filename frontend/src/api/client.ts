import type {
  ActivityPayload,
  Activity,
  ErrorResponse,
  Project,
  ProjectPayload,
  ProjectSummary,
} from './types';

const API_BASE_PATH = '/api/v1';
const UNEXPECTED_ERROR_CODE = 'UNEXPECTED_ERROR';

export class ApiError extends Error {
  readonly status: number;
  readonly body: ErrorResponse;

  constructor(status: number, body: ErrorResponse) {
    super(body.message);
    this.name = 'ApiError';
    this.status = status;
    this.body = body;
  }
}

function isErrorResponse(value: unknown): value is ErrorResponse {
  return (
    typeof value === 'object' &&
    value !== null &&
    'code' in value &&
    'message' in value &&
    'details' in value
  );
}

async function toApiError(response: Response): Promise<ApiError> {
  const body: unknown = await response.json().catch(() => null);
  if (isErrorResponse(body)) {
    return new ApiError(response.status, body);
  }
  return new ApiError(response.status, {
    code: UNEXPECTED_ERROR_CODE,
    message: `El servidor respondió ${response.status} ${response.statusText}`,
    details: [],
  });
}

async function send(path: string, init: RequestInit = {}): Promise<Response> {
  const response = await fetch(`${API_BASE_PATH}${path}`, {
    ...init,
    headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
  });
  if (!response.ok) {
    throw await toApiError(response);
  }
  return response;
}

async function getJson<T>(path: string): Promise<T> {
  const response = await send(path);
  return (await response.json()) as T;
}

async function sendJson<T>(method: 'POST' | 'PUT', path: string, payload: unknown): Promise<T> {
  const response = await send(path, { method, body: JSON.stringify(payload) });
  return (await response.json()) as T;
}

async function remove(path: string): Promise<void> {
  await send(path, { method: 'DELETE' });
}

const projectPath = (projectId: number) => `/projects/${projectId}`;
const activitiesPath = (projectId: number) => `${projectPath(projectId)}/activities`;
const activityPath = (projectId: number, activityId: number) =>
  `${activitiesPath(projectId)}/${activityId}`;

export const projectsApi = {
  list: () => getJson<ProjectSummary[]>('/projects'),
  get: (projectId: number) => getJson<Project>(projectPath(projectId)),
  create: (payload: ProjectPayload) => sendJson<Project>('POST', '/projects', payload),
  update: (projectId: number, payload: ProjectPayload) =>
    sendJson<Project>('PUT', projectPath(projectId), payload),
  remove: (projectId: number) => remove(projectPath(projectId)),
};

export const activitiesApi = {
  create: (projectId: number, payload: ActivityPayload) =>
    sendJson<Activity>('POST', activitiesPath(projectId), payload),
  update: (projectId: number, activityId: number, payload: ActivityPayload) =>
    sendJson<Activity>('PUT', activityPath(projectId, activityId), payload),
  remove: (projectId: number, activityId: number) => remove(activityPath(projectId, activityId)),
};
