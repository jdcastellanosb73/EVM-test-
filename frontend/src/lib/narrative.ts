/**
 * Plain-language reading of each indicator. The wording and the tone come from the status the
 * API decided on the unrounded value, never from the displayed number: a CPI of 0.99996 shown
 * as "1,0000" still reads as over budget.
 */

import type {
  CostPerformanceStatus,
  Indicators,
  PerformanceIndex,
  SchedulePerformanceStatus,
} from '../api/types';
import { absoluteAmount, formatIndex, formatMoney } from './format';
import { COST_STATUS, SCHEDULE_STATUS, type Tone } from './status';

export interface IndicatorReading {
  label: string;
  tone: Tone;
  sentence: string;
}

const NO_ESTIMATE_LABEL = 'Sin estimación';
const NO_FINAL_ESTIMATE_SENTENCE =
  'Sin estimado final (EAC) no se puede saber si sobrará o faltará dinero.';

const ESTIMATE_LABELS: Record<CostPerformanceStatus, string> = {
  UNDER_BUDGET: 'Dentro del presupuesto',
  ON_BUDGET: 'Igual al presupuesto',
  OVER_BUDGET: 'Por encima del presupuesto',
  NOT_APPLICABLE: NO_ESTIMATE_LABEL,
};

const VARIANCE_LABELS: Record<CostPerformanceStatus, string> = {
  UNDER_BUDGET: 'Sobra presupuesto',
  ON_BUDGET: 'Presupuesto exacto',
  OVER_BUDGET: 'Falta presupuesto',
  NOT_APPLICABLE: NO_ESTIMATE_LABEL,
};

const NOT_ENOUGH_DATA_VERDICT =
  'Aún sin datos suficientes: registra avance y costo de las actividades para evaluar el proyecto.';

function noEstimate(sentence: string): IndicatorReading {
  return { label: NO_ESTIMATE_LABEL, tone: 'neutral', sentence };
}

export function readCostPerformance(
  index: PerformanceIndex<CostPerformanceStatus>,
): IndicatorReading {
  const value = formatIndex(index.value);
  const sentences: Record<CostPerformanceStatus, string> = {
    UNDER_BUDGET: `Por cada peso gastado se obtienen ${value} en trabajo: gasta menos de lo que avanza.`,
    ON_BUDGET: 'Cada peso gastado produce exactamente un peso de trabajo.',
    OVER_BUDGET: `Por cada peso gastado se obtienen ${value} en trabajo: gasta más de lo que avanza.`,
    NOT_APPLICABLE: 'Aún no hay costo registrado: no se puede medir la eficiencia del gasto.',
  };
  return { ...COST_STATUS[index.status], sentence: sentences[index.status] };
}

export function readSchedulePerformance(
  index: PerformanceIndex<SchedulePerformanceStatus>,
): IndicatorReading {
  const value = formatIndex(index.value);
  const sentences: Record<SchedulePerformanceStatus, string> = {
    AHEAD_OF_SCHEDULE: `Lleva ${value} de avance por cada peso planificado: va por delante del plan.`,
    ON_SCHEDULE: 'Avanza exactamente al ritmo planificado.',
    BEHIND_SCHEDULE: `Lleva ${value} de avance por cada peso planificado: va por detrás del plan.`,
    NOT_APPLICABLE: 'A la fecha de corte no había avance planificado: no se puede medir el ritmo.',
  };
  return { ...SCHEDULE_STATUS[index.status], sentence: sentences[index.status] };
}

/** EAC = BAC / CPI, so its reading follows the cost status the API returned. */
export function readEstimateAtCompletion(indicators: Indicators): IndicatorReading {
  if (indicators.eac === null) {
    return noEstimate('Hace falta costo y avance registrados para proyectar el costo final.');
  }
  const { status } = indicators.cpi;
  return {
    label: ESTIMATE_LABELS[status],
    tone: COST_STATUS[status].tone,
    sentence: `Si sigue igual, costará ${formatMoney(indicators.eac)} frente a un presupuesto de ${formatMoney(indicators.bac)}.`,
  };
}

/** VAC = BAC − EAC: positive means money left over, negative means money missing. */
export function readVarianceAtCompletion(indicators: Indicators): IndicatorReading {
  if (indicators.vac === null) {
    return noEstimate(NO_FINAL_ESTIMATE_SENTENCE);
  }
  const { status } = indicators.cpi;
  const amount = formatMoney(absoluteAmount(indicators.vac));
  const sentences: Record<CostPerformanceStatus, string> = {
    UNDER_BUDGET: `Al terminar sobrarían ${amount} del presupuesto.`,
    ON_BUDGET: 'Al terminar se gastaría exactamente el presupuesto.',
    OVER_BUDGET: `Al terminar faltarían ${amount} para cubrir el costo.`,
    NOT_APPLICABLE: NO_FINAL_ESTIMATE_SENTENCE,
  };
  return {
    label: VARIANCE_LABELS[status],
    tone: COST_STATUS[status].tone,
    sentence: sentences[status],
  };
}

/** Tone of a set of indicators: bad if cost or schedule is bad, neutral if neither is measurable. */
export function readOverallTone(indicators: Indicators): Tone {
  const tones = [
    COST_STATUS[indicators.cpi.status].tone,
    SCHEDULE_STATUS[indicators.spi.status].tone,
  ];
  if (tones.includes('bad')) {
    return 'bad';
  }
  return tones.every((tone) => tone === 'neutral') ? 'neutral' : 'good';
}

export const PROJECT_HEALTH_LABELS: Record<Tone, string> = {
  good: 'En control',
  bad: 'Requiere atención',
  neutral: 'Sin datos suficientes',
};

/** One-sentence verdict built only from the statuses the API returned. */
export function readProjectVerdict(indicators: Indicators): string {
  const tone = readOverallTone(indicators);
  if (tone === 'neutral') {
    return NOT_ENOUGH_DATA_VERDICT;
  }
  const cost = COST_STATUS[indicators.cpi.status].label.toLowerCase();
  const schedule = SCHEDULE_STATUS[indicators.spi.status].label.toLowerCase();
  const prefix = tone === 'bad' ? PROJECT_HEALTH_LABELS.bad : 'Va según lo esperado';
  return `${prefix}: ${cost} y ${schedule}.`;
}
