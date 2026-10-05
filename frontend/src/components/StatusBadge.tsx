import { ArrowDownRight, ArrowUpRight, Minus, type LucideIcon } from 'lucide-react';
import type {
  CostPerformanceStatus,
  PerformanceIndex,
  SchedulePerformanceStatus,
} from '../api/types';
import { formatIndex } from '../lib/format';
import { COST_STATUS, SCHEDULE_STATUS, type StatusPresentation, type Tone } from '../lib/status';

const TONE_ICONS: Record<Tone, LucideIcon> = {
  good: ArrowUpRight,
  bad: ArrowDownRight,
  neutral: Minus,
};

interface BadgeProps {
  presentation: StatusPresentation;
  value: string | null;
  acronym: string;
}

/** Traffic light: color, arrow, value and words together, never color alone. */
function Badge({ presentation, value, acronym }: BadgeProps) {
  const shownValue = formatIndex(value);
  const Icon = TONE_ICONS[presentation.tone];
  return (
    <span
      className={`status-pill tone-${presentation.tone}`}
      title={`${acronym} ${shownValue}: ${presentation.label}`}
    >
      <Icon aria-hidden="true" />
      <span className="status-pill__value">{shownValue}</span>
      <span>{presentation.label}</span>
    </span>
  );
}

export function CpiBadge({ index }: { index: PerformanceIndex<CostPerformanceStatus> }) {
  return <Badge presentation={COST_STATUS[index.status]} value={index.value} acronym="CPI" />;
}

export function SpiBadge({ index }: { index: PerformanceIndex<SchedulePerformanceStatus> }) {
  return <Badge presentation={SCHEDULE_STATUS[index.status]} value={index.value} acronym="SPI" />;
}
