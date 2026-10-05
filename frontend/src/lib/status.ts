/** Traffic-light meaning of the statuses the API returns. The API decides the status. */

import type { CostPerformanceStatus, SchedulePerformanceStatus } from '../api/types';

export type Tone = 'good' | 'bad' | 'neutral';

export interface StatusPresentation {
  label: string;
  tone: Tone;
}

export const COST_STATUS: Record<CostPerformanceStatus, StatusPresentation> = {
  UNDER_BUDGET: { label: 'Bajo presupuesto', tone: 'good' },
  ON_BUDGET: { label: 'En presupuesto', tone: 'good' },
  OVER_BUDGET: { label: 'Sobre presupuesto', tone: 'bad' },
  NOT_APPLICABLE: { label: 'Sin costo registrado', tone: 'neutral' },
};

export const SCHEDULE_STATUS: Record<SchedulePerformanceStatus, StatusPresentation> = {
  AHEAD_OF_SCHEDULE: { label: 'Adelantado', tone: 'good' },
  ON_SCHEDULE: { label: 'A tiempo', tone: 'good' },
  BEHIND_SCHEDULE: { label: 'Atrasado', tone: 'bad' },
  NOT_APPLICABLE: { label: 'Sin avance planificado', tone: 'neutral' },
};
