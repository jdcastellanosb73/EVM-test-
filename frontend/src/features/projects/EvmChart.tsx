import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Text,
  Tooltip,
  XAxis,
  YAxis,
  type TooltipContentProps,
  type XAxisTickContentProps,
} from 'recharts';
import type { Activity, Indicators } from '../../api/types';
import { formatAxisAmount, formatMoney } from '../../lib/format';

const CHART_HEIGHT = 300;
const X_AXIS_HEIGHT = 48;
const TICK_FONT_SIZE = 12;
const TICK_HORIZONTAL_PADDING = 8;
const CHART_MARGIN = { top: 8, right: 8, left: 8, bottom: 8 };
const Y_AXIS_WIDTH = 64;
const BAR_CORNER_RADIUS = 3;
const BAR_MAX_WIDTH = 26;
const BAR_GAP = 3;
/** Rounded top corners only, so bars stay flush with the axis. */
const BAR_RADIUS: [number, number, number, number] = [BAR_CORNER_RADIUS, BAR_CORNER_RADIUS, 0, 0];

const SERIES = [
  { key: 'pv', name: 'Planificado (PV)', color: 'var(--chart-pv)' },
  { key: 'ev', name: 'Ganado (EV)', color: 'var(--chart-ev)' },
  { key: 'ac', name: 'Costo real (AC)', color: 'var(--chart-ac)' },
] as const;

type SeriesKey = (typeof SERIES)[number]['key'];

interface ChartRow {
  name: string;
  pv: number;
  ev: number;
  ac: number;
  indicators: Indicators;
}

/** Bar heights need numbers; the exact strings stay in `indicators` for the tooltip. */
function toChartRow(activity: Activity): ChartRow {
  const { indicators } = activity;
  return {
    name: activity.name,
    pv: Number(indicators.pv),
    ev: Number(indicators.ev),
    ac: Number(indicators.ac),
    indicators,
  };
}

/** Activity names wrap within their own band so they never overlap on narrow screens. */
function ActivityTick({ x, y, payload, width, visibleTicksCount }: XAxisTickContentProps) {
  const bandWidth = Number(width) / visibleTicksCount - TICK_HORIZONTAL_PADDING;
  return (
    <Text
      x={x}
      y={y}
      width={bandWidth}
      textAnchor="middle"
      verticalAnchor="start"
      fontSize={TICK_FONT_SIZE}
      fill="var(--color-muted)"
    >
      {String(payload.value)}
    </Text>
  );
}

function ChartTooltip({ active, payload, label }: TooltipContentProps) {
  const row = payload[0]?.payload as ChartRow | undefined;
  if (!active || row === undefined) {
    return null;
  }
  return (
    <div className="chart-tooltip">
      <p className="chart-tooltip-title">{label}</p>
      <dl>
        {SERIES.map((series) => (
          <div key={series.key} className="chart-tooltip-row">
            <dt>
              <span className="chart-swatch" style={{ background: series.color }} />
              {series.name}
            </dt>
            <dd>{formatMoney(row.indicators[series.key satisfies SeriesKey])}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}

export function EvmChart({ activities }: { activities: Activity[] }) {
  const rows = activities.map(toChartRow);
  return (
    <section className="card chart-card" aria-labelledby="evm-chart-title">
      <header className="card-heading">
        <div>
          <h3 id="evm-chart-title">Rendimiento por actividad</h3>
          <p>Valor planificado (PV), valor ganado (EV) y costo real (AC)</p>
        </div>
        <ul className="legend" aria-label="Series de la gráfica">
          {SERIES.map((series) => (
            <li key={series.key}>
              <span className="legend-swatch" style={{ background: series.color }} />
              {series.name}
            </li>
          ))}
        </ul>
      </header>
      <p className="chart-guide">
        Cuando la barra de EV es más baja que la de AC, la actividad gasta más de lo que avanza.
        Cuando es más baja que la de PV, va atrasada.
      </p>
      <figure className="chart-figure">
        <ResponsiveContainer width="100%" height={CHART_HEIGHT}>
          <BarChart data={rows} margin={CHART_MARGIN} barGap={BAR_GAP}>
            <CartesianGrid stroke="var(--chart-grid)" vertical={false} />
            <XAxis
              dataKey="name"
              interval={0}
              height={X_AXIS_HEIGHT}
              tick={ActivityTick}
              tickLine={false}
              stroke="var(--chart-grid)"
            />
            <YAxis
              tickFormatter={formatAxisAmount}
              width={Y_AXIS_WIDTH}
              tick={{ fontSize: TICK_FONT_SIZE, fill: 'var(--color-subtle)' }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip content={ChartTooltip} cursor={{ fill: 'var(--color-neutral-surface)' }} />
            {SERIES.map((series) => (
              <Bar
                key={series.key}
                dataKey={series.key}
                name={series.name}
                fill={series.color}
                radius={BAR_RADIUS}
                maxBarSize={BAR_MAX_WIDTH}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
        <figcaption className="visually-hidden">
          Gráfica de barras agrupadas con el valor planificado, el valor ganado y el costo real de
          cada actividad. Los mismos datos están en la tabla de actividades.
        </figcaption>
      </figure>
    </section>
  );
}
