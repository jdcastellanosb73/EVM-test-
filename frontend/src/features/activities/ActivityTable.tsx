import { Pencil, Trash2 } from 'lucide-react';
import type { Activity, Indicators } from '../../api/types';
import { CpiBadge, SpiBadge } from '../../components/StatusBadge';
import { MISSING_VALUE, formatMoney, formatPercent, isNegative } from '../../lib/format';
import { readOverallTone } from '../../lib/narrative';

interface ActivityTableProps {
  activities: Activity[];
  projectIndicators: Indicators;
  onEdit: (activity: Activity) => void;
  onDelete: (activity: Activity) => void;
  isDeleting: boolean;
}

interface Column {
  label: string;
  numeric: boolean;
}

const COLUMNS: Column[] = [
  { label: 'Actividad', numeric: false },
  { label: 'Avance real / plan', numeric: false },
  { label: 'BAC', numeric: true },
  { label: 'AC', numeric: true },
  { label: 'PV', numeric: true },
  { label: 'EV', numeric: true },
  { label: 'CV', numeric: true },
  { label: 'SV', numeric: true },
  { label: 'CPI', numeric: false },
  { label: 'SPI', numeric: false },
  { label: 'EAC', numeric: true },
  { label: 'VAC', numeric: true },
];

const CONSOLIDATED_PROGRESS_LABEL = 'El avance del proyecto se consolida en PV y EV';
const NO_ESTIMATE_LABEL = 'Sin estimación: el CPI no existe (AC = 0) o es 0 (sin avance real)';
const NO_ACTIONS_LABEL = 'Sin acciones';

function MoneyCell({ value }: { value: string | null }) {
  return (
    <td className={isNegative(value) ? 'numeric negative' : 'numeric'}>{formatMoney(value)}</td>
  );
}

function NotApplicableCell({ label, numeric = false }: { label: string; numeric?: boolean }) {
  return (
    <td className={numeric ? 'numeric' : undefined} title={label}>
      <span aria-hidden="true">{MISSING_VALUE}</span>
      <span className="visually-hidden">{label}</span>
    </td>
  );
}

/** Bar of the actual progress with a tick where the plan says it should be. */
function ProgressCell({ activity }: { activity: Activity }) {
  const actual = formatPercent(activity.actual_percent);
  const planned = formatPercent(activity.planned_percent);
  return (
    <td aria-label={`Avance real ${actual} de ${planned} planificado`}>
      <div className="progress-cell">
        <span className="progress-track" aria-hidden="true">
          <span className="progress-actual" style={{ width: `${activity.actual_percent}%` }} />
          <span className="progress-plan" style={{ left: `${activity.planned_percent}%` }} />
        </span>
        <strong>{actual}</strong>
        <small>/ {planned}</small>
      </div>
    </td>
  );
}

/** EAC and VAC are null when the CPI is undefined or 0: say why instead of a bare dash. */
function EstimateCell({ value }: { value: string | null }) {
  return value === null ? (
    <NotApplicableCell label={NO_ESTIMATE_LABEL} numeric />
  ) : (
    <MoneyCell value={value} />
  );
}

function IndicatorCells({ indicators }: { indicators: Indicators }) {
  return (
    <>
      <MoneyCell value={indicators.ac} />
      <MoneyCell value={indicators.pv} />
      <MoneyCell value={indicators.ev} />
      <MoneyCell value={indicators.cv} />
      <MoneyCell value={indicators.sv} />
      <td>
        <CpiBadge index={indicators.cpi} />
      </td>
      <td>
        <SpiBadge index={indicators.spi} />
      </td>
      <EstimateCell value={indicators.eac} />
      <EstimateCell value={indicators.vac} />
    </>
  );
}

function NameCell({ name, indicators }: { name: string; indicators: Indicators }) {
  return (
    <th scope="row">
      <span className="row-name">
        <span className={`row-dot tone-${readOverallTone(indicators)}`} aria-hidden="true" />
        {name}
      </span>
    </th>
  );
}

export function ActivityTable({
  activities,
  projectIndicators,
  onEdit,
  onDelete,
  isDeleting,
}: ActivityTableProps) {
  return (
    <div className="table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            {COLUMNS.map((column) => (
              <th key={column.label} scope="col" className={column.numeric ? 'numeric' : undefined}>
                {column.label}
              </th>
            ))}
            <th scope="col">
              <span className="visually-hidden">Acciones</span>
            </th>
          </tr>
        </thead>
        <tbody>
          {activities.map((activity) => (
            <tr key={activity.id}>
              <NameCell name={activity.name} indicators={activity.indicators} />
              <ProgressCell activity={activity} />
              <MoneyCell value={activity.budget_at_completion} />
              <IndicatorCells indicators={activity.indicators} />
              <td className="row-actions">
                <button
                  type="button"
                  className="button-icon"
                  aria-label={`Editar ${activity.name}`}
                  title="Editar"
                  onClick={() => onEdit(activity)}
                >
                  <Pencil aria-hidden="true" />
                </button>
                <button
                  type="button"
                  className="button-icon danger"
                  aria-label={`Eliminar ${activity.name}`}
                  title="Eliminar"
                  disabled={isDeleting}
                  onClick={() => onDelete(activity)}
                >
                  <Trash2 aria-hidden="true" />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr>
            <NameCell name="Total del proyecto" indicators={projectIndicators} />
            <NotApplicableCell label={CONSOLIDATED_PROGRESS_LABEL} />
            <MoneyCell value={projectIndicators.bac} />
            <IndicatorCells indicators={projectIndicators} />
            <NotApplicableCell label={NO_ACTIONS_LABEL} />
          </tr>
        </tfoot>
      </table>
    </div>
  );
}
