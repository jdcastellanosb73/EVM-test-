import type { Indicators } from '../../api/types';
import { CpiBadge, SpiBadge } from '../../components/StatusBadge';
import { formatMoney, isNegative } from '../../lib/format';
import { COST_STATUS, SCHEDULE_STATUS } from '../../lib/status';

interface AmountProps {
  label: string;
  value: string | null;
  hint: string;
}

function Amount({ label, value, hint }: AmountProps) {
  return (
    <div className="amount">
      <dt>{label}</dt>
      <dd className={isNegative(value) ? 'negative' : undefined}>{formatMoney(value)}</dd>
      <dd className="amount-hint">{hint}</dd>
    </div>
  );
}

/** One-sentence verdict built only from the statuses the API returned. */
function verdict(indicators: Indicators): string {
  const cost = COST_STATUS[indicators.cpi.status];
  const schedule = SCHEDULE_STATUS[indicators.spi.status];
  const needsAttention = cost.tone === 'bad' || schedule.tone === 'bad';
  const prefix = needsAttention ? 'Requiere atención' : 'Va según lo esperado';
  return `${prefix}: ${cost.label.toLowerCase()} y ${schedule.label.toLowerCase()}.`;
}

export function ProjectIndicators({ indicators }: { indicators: Indicators }) {
  return (
    <section className="panel" aria-labelledby="project-indicators-title">
      <h2 id="project-indicators-title">Consolidado del proyecto</h2>
      <p className="verdict">{verdict(indicators)}</p>
      <div className="index-cards">
        <div className="index-card">
          <h3>Costo · CPI</h3>
          <CpiBadge index={indicators.cpi} />
          <p className="amount-hint">Valor obtenido por cada peso gastado (EV / AC)</p>
        </div>
        <div className="index-card">
          <h3>Cronograma · SPI</h3>
          <SpiBadge index={indicators.spi} />
          <p className="amount-hint">Avance logrado por cada peso planificado (EV / PV)</p>
        </div>
      </div>
      <dl className="amounts">
        <Amount label="Presupuesto (BAC)" value={indicators.bac} hint="Total planificado" />
        <Amount label="Valor planificado (PV)" value={indicators.pv} hint="Lo que debía ir hecho" />
        <Amount label="Valor ganado (EV)" value={indicators.ev} hint="Lo que realmente se hizo" />
        <Amount label="Costo real (AC)" value={indicators.ac} hint="Lo que se ha gastado" />
        <Amount label="Variación de costo (CV)" value={indicators.cv} hint="EV − AC" />
        <Amount label="Variación de cronograma (SV)" value={indicators.sv} hint="EV − PV" />
        <Amount
          label="Estimado al terminar (EAC)"
          value={indicators.eac}
          hint="Costo final si sigue igual"
        />
        <Amount
          label="Variación al terminar (VAC)"
          value={indicators.vac}
          hint="BAC − EAC: sobra (+) o falta (−)"
        />
      </dl>
    </section>
  );
}
