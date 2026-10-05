import { BarChart3, CalendarDays, Scale, WalletCards } from 'lucide-react';
import type { Indicators } from '../../api/types';
import { IndicatorCard } from '../../components/IndicatorCard';
import { formatIndex, formatMoney, isNegative } from '../../lib/format';
import {
  readCostPerformance,
  readEstimateAtCompletion,
  readSchedulePerformance,
  readVarianceAtCompletion,
} from '../../lib/narrative';

interface AmountProps {
  label: string;
  value: string | null;
  hint: string;
}

function Amount({ label, value, hint }: AmountProps) {
  return (
    <div className="amount-card">
      <dt>{label}</dt>
      <dd className={isNegative(value) ? 'amount-value negative' : 'amount-value'}>
        {formatMoney(value)}
      </dd>
      <dd className="amount-hint">{hint}</dd>
    </div>
  );
}

export function ProjectIndicators({ indicators }: { indicators: Indicators }) {
  return (
    <section aria-labelledby="project-indicators-title">
      <header className="section-heading">
        <div>
          <h2 id="project-indicators-title">Resumen ejecutivo</h2>
          <p>
            Indicadores consolidados del proyecto: se suman los montos y se recalculan los índices
          </p>
        </div>
      </header>
      <div className="metric-grid">
        <IndicatorCard
          title="CPI · Costos (EV / AC)"
          value={formatIndex(indicators.cpi.value)}
          reading={readCostPerformance(indicators.cpi)}
          icon={WalletCards}
        />
        <IndicatorCard
          title="SPI · Cronograma (EV / PV)"
          value={formatIndex(indicators.spi.value)}
          reading={readSchedulePerformance(indicators.spi)}
          icon={CalendarDays}
        />
        <IndicatorCard
          title="EAC · Estimado final"
          value={formatMoney(indicators.eac)}
          reading={readEstimateAtCompletion(indicators)}
          icon={BarChart3}
        />
        <IndicatorCard
          title="VAC · Variación final"
          value={formatMoney(indicators.vac)}
          reading={readVarianceAtCompletion(indicators)}
          icon={Scale}
        />
      </div>
      <dl className="amount-grid">
        <Amount label="Presupuesto (BAC)" value={indicators.bac} hint="Total planificado" />
        <Amount label="Valor planificado (PV)" value={indicators.pv} hint="Lo que debía ir hecho" />
        <Amount label="Valor ganado (EV)" value={indicators.ev} hint="Lo que realmente se hizo" />
        <Amount label="Costo real (AC)" value={indicators.ac} hint="Lo que se ha gastado" />
        <Amount label="Variación de costo (CV)" value={indicators.cv} hint="EV − AC" />
        <Amount label="Variación de cronograma (SV)" value={indicators.sv} hint="EV − PV" />
      </dl>
    </section>
  );
}
