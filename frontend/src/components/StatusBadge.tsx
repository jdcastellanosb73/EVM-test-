import type {
  CostPerformanceStatus,
  PerformanceIndex,
  SchedulePerformanceStatus,
} from '../api/types';
import { formatIndex } from '../lib/format';
import { COST_STATUS, SCHEDULE_STATUS, type StatusPresentation } from '../lib/status';

interface BadgeProps {
  presentation: StatusPresentation;
  value: string | null;
  acronym: string;
}

function Badge({ presentation, value, acronym }: BadgeProps) {
  const shownValue = formatIndex(value);
  return (
    <span
      className={`badge badge-${presentation.tone}`}
      title={`${acronym} ${shownValue}: ${presentation.label}`}
    >
      <span className="badge-dot" aria-hidden="true" />
      <span className="badge-value">{shownValue}</span>
      <span className="badge-label">{presentation.label}</span>
    </span>
  );
}

export function CpiBadge({ index }: { index: PerformanceIndex<CostPerformanceStatus> }) {
  return <Badge presentation={COST_STATUS[index.status]} value={index.value} acronym="CPI" />;
}

export function SpiBadge({ index }: { index: PerformanceIndex<SchedulePerformanceStatus> }) {
  return <Badge presentation={SCHEDULE_STATUS[index.status]} value={index.value} acronym="SPI" />;
}
