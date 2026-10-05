import { CalendarDays, WalletCards, type LucideIcon } from 'lucide-react';
import type { ReactNode } from 'react';
import type { Indicators } from '../../api/types';
import { CpiBadge, SpiBadge } from '../../components/StatusBadge';
import { PROJECT_HEALTH_LABELS, readOverallTone } from '../../lib/narrative';
import { COST_STATUS, SCHEDULE_STATUS, type Tone } from '../../lib/status';

interface HealthRowProps {
  title: string;
  interpretation: string;
  tone: Tone;
  icon: LucideIcon;
  badge: ReactNode;
}

function HealthRow({ title, interpretation, tone, icon: Icon, badge }: HealthRowProps) {
  return (
    <div className="health-row">
      <span className={`health-icon tone-${tone}`}>
        <Icon aria-hidden="true" />
      </span>
      <div className="health-row__text">
        <strong>{title}</strong>
        <span>{interpretation}</span>
      </div>
      {badge}
    </div>
  );
}

/** CPI and SPI side by side, each with the interpretation the API returns. */
export function ProjectHealth({ indicators }: { indicators: Indicators }) {
  const tone = readOverallTone(indicators);
  return (
    <section className="card health-card" aria-labelledby="project-health-title">
      <header className="card-heading">
        <div>
          <h3 id="project-health-title">Salud del proyecto</h3>
          <p>Lectura rápida de costo y cronograma</p>
        </div>
        <span className={`health-badge tone-${tone}`}>{PROJECT_HEALTH_LABELS[tone]}</span>
      </header>
      <HealthRow
        title="Costos (CPI)"
        interpretation={indicators.cpi.interpretation}
        tone={COST_STATUS[indicators.cpi.status].tone}
        icon={WalletCards}
        badge={<CpiBadge index={indicators.cpi} />}
      />
      <HealthRow
        title="Cronograma (SPI)"
        interpretation={indicators.spi.interpretation}
        tone={SCHEDULE_STATUS[indicators.spi.status].tone}
        icon={CalendarDays}
        badge={<SpiBadge index={indicators.spi} />}
      />
      <div className="health-callout">
        <span>Cómo leerlo</span>
        <p>
          Un índice mayor a 1 es favorable y uno menor a 1 requiere atención. El estado se decide
          con el valor exacto que calcula el API, no con el número redondeado.
        </p>
      </div>
    </section>
  );
}
