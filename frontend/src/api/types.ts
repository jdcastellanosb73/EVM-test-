/** Contract of the EVM Tracker API (/api-docs). Amounts travel as decimal strings. */

export type DecimalString = string;

export type CostPerformanceStatus = 'UNDER_BUDGET' | 'ON_BUDGET' | 'OVER_BUDGET' | 'NOT_APPLICABLE';

export type SchedulePerformanceStatus =
  'AHEAD_OF_SCHEDULE' | 'ON_SCHEDULE' | 'BEHIND_SCHEDULE' | 'NOT_APPLICABLE';

export interface PerformanceIndex<Status> {
  value: DecimalString | null;
  status: Status;
  /** Plain-language reading of the status, written by the API. */
  interpretation: string;
}

export interface Indicators {
  bac: DecimalString;
  pv: DecimalString;
  ev: DecimalString;
  ac: DecimalString;
  cv: DecimalString;
  sv: DecimalString;
  cpi: PerformanceIndex<CostPerformanceStatus>;
  spi: PerformanceIndex<SchedulePerformanceStatus>;
  eac: DecimalString | null;
  vac: DecimalString | null;
}

export interface Activity {
  id: number;
  project_id: number;
  name: string;
  budget_at_completion: DecimalString;
  planned_percent: DecimalString;
  actual_percent: DecimalString;
  actual_cost: DecimalString;
  created_at: string;
  updated_at: string;
  indicators: Indicators;
}

export interface ProjectSummary {
  id: number;
  name: string;
  description: string | null;
  cutoff_date: string | null;
  activity_count: number;
  indicators: Indicators;
}

export interface Project {
  id: number;
  name: string;
  description: string | null;
  cutoff_date: string | null;
  created_at: string;
  updated_at: string;
  activities: Activity[];
  indicators: Indicators;
}

export interface ProjectPayload {
  name: string;
  description: string | null;
  cutoff_date: string | null;
}

export interface ActivityPayload {
  name: string;
  budget_at_completion: DecimalString;
  planned_percent: DecimalString;
  actual_percent: DecimalString;
  actual_cost: DecimalString;
}

interface ErrorDetail {
  field: string | null;
  message: string;
}

export interface ErrorResponse {
  code: string;
  message: string;
  details: ErrorDetail[];
}
