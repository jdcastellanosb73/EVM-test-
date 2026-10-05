import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { activitiesApi, projectsApi } from './client';
import type { ActivityPayload, ProjectPayload } from './types';

const projectKeys = {
  all: ['projects'] as const,
  list: () => [...projectKeys.all, 'list'] as const,
  detail: (projectId: number) => [...projectKeys.all, 'detail', projectId] as const,
};

export function useProjects() {
  return useQuery({ queryKey: projectKeys.list(), queryFn: projectsApi.list });
}

export function useProject(projectId: number) {
  return useQuery({
    queryKey: projectKeys.detail(projectId),
    queryFn: () => projectsApi.get(projectId),
  });
}

/** Every write changes the indicators of the list and the detail: refetch both from the API. */
function useRefreshProjects() {
  const queryClient = useQueryClient();
  return () => queryClient.invalidateQueries({ queryKey: projectKeys.all });
}

export function useSaveProject(projectId?: number) {
  const refreshProjects = useRefreshProjects();
  return useMutation({
    mutationFn: (payload: ProjectPayload) =>
      projectId === undefined
        ? projectsApi.create(payload)
        : projectsApi.update(projectId, payload),
    onSuccess: refreshProjects,
  });
}

export function useDeleteProject() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: projectsApi.remove,
    onSuccess: (_, projectId) => {
      queryClient.removeQueries({ queryKey: projectKeys.detail(projectId) });
      return queryClient.invalidateQueries({ queryKey: projectKeys.list() });
    },
  });
}

export function useSaveActivity(projectId: number, activityId?: number) {
  const refreshProjects = useRefreshProjects();
  return useMutation({
    mutationFn: (payload: ActivityPayload) =>
      activityId === undefined
        ? activitiesApi.create(projectId, payload)
        : activitiesApi.update(projectId, activityId, payload),
    onSuccess: refreshProjects,
  });
}

export function useDeleteActivity(projectId: number) {
  const refreshProjects = useRefreshProjects();
  return useMutation({
    mutationFn: (activityId: number) => activitiesApi.remove(projectId, activityId),
    onSuccess: refreshProjects,
  });
}
