import type { LucideIcon } from 'lucide-react';
import type { IndicatorReading } from '../lib/narrative';

interface IndicatorCardProps {
  title: string;
  value: string;
  reading: IndicatorReading;
  icon: LucideIcon;
}

/** The number never appears alone: it always carries its status label, color and a sentence. */
export function IndicatorCard({ title, value, reading, icon: Icon }: IndicatorCardProps) {
  return (
    <article className={`metric-card tone-${reading.tone}`}>
      <header className="metric-card__top">
        <h3>{title}</h3>
        <Icon aria-hidden="true" />
      </header>
      <p className="metric-card__value">{value}</p>
      <p className="metric-card__status">
        <span className="tone-dot" aria-hidden="true" />
        {reading.label}
      </p>
      <p className="metric-card__detail">{reading.sentence}</p>
    </article>
  );
}
