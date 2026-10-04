import type { Activity, Indicators } from '../../api/types';
import { CpiBadge, SpiBadge } from '../../components/StatusBadge';
import { MISSING_VALUE, formatMoney, formatPercent, isNegative } from '../../lib/format';

interface ActivityTableProps {
  activities: Activity[];
  projectIndicators: Indicators;
  onEdit: (activity: Activity) => void;
  onDelete: (activity: Activity) => void;
  isDeleting: boolean;
}

function MoneyCell({ value }: { value: string | null }) {
  return (
    <td className={isNegative(value) ? 'numeric negative' : 'numeric'}>{formatMoney(value)}</td>
  );
}

function NotApplicableCell({ label }: { label: string }) {
  return (
    <td className="numeric" title={label}>
      <span aria-hidden="true">{MISSING_VALUE}</span>
      <span className="visually-hidden">{label}</span>
    </td>
  );
}

function IndicatorCells({ indicators }: { indicators: Indicators }) {
  return (
    <>
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
      <MoneyCell value={indicators.eac} />
      <MoneyCell value={indicators.vac} />
    </>
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
    <div className="table-scroll">
      <table className="data-table">
        <thead>
          <tr>
            <th scope="col">Actividad</th>
            <th scope="col" className="numeric">
              BAC
            </th>
            <th scope="col" className="numeric">
              % plan
            </th>
            <th scope="col" className="numeric">
              % real
            </th>
            <th scope="col" className="numeric">
              AC
            </th>
            <th scope="col" className="numeric">
              PV
            </th>
            <th scope="col" className="numeric">
              EV
            </th>
            <th scope="col" className="numeric">
              CV
            </th>
            <th scope="col" className="numeric">
              SV
            </th>
            <th scope="col">CPI</th>
            <th scope="col">SPI</th>
            <th scope="col" className="numeric">
              EAC
            </th>
            <th scope="col" className="numeric">
              VAC
            </th>
            <th scope="col">
              <span className="visually-hidden">Acciones</span>
            </th>
          </tr>
        </thead>
        <tbody>
          {activities.map((activity) => (
            <tr key={activity.id}>
              <th scope="row">{activity.name}</th>
              <MoneyCell value={activity.budget_at_completion} />
              <td className="numeric">{formatPercent(activity.planned_percent)}</td>
              <td className="numeric">{formatPercent(activity.actual_percent)}</td>
              <MoneyCell value={activity.actual_cost} />
              <IndicatorCells indicators={activity.indicators} />
              <td className="row-actions">
                <button type="button" className="button-link" onClick={() => onEdit(activity)}>
                  Editar
                </button>
                <button
                  type="button"
                  className="button-link danger"
                  disabled={isDeleting}
                  onClick={() => onDelete(activity)}
                >
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr>
            <th scope="row">Total del proyecto</th>
            <MoneyCell value={projectIndicators.bac} />
            <NotApplicableCell label="El avance se consolida en PV y EV" />
            <NotApplicableCell label="El avance se consolida en PV y EV" />
            <MoneyCell value={projectIndicators.ac} />
            <IndicatorCells indicators={projectIndicators} />
            <NotApplicableCell label="Sin acciones" />
          </tr>
        </tfoot>
      </table>
    </div>
  );
}
