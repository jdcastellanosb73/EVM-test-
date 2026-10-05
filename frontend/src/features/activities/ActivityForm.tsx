import { useState, type FormEvent } from 'react';
import { useSaveActivity } from '../../api/queries';
import type { Activity, ActivityPayload } from '../../api/types';
import { AlertMessage } from '../../components/Feedback';
import { FormActions } from '../../components/FormActions';
import { FormField } from '../../components/FormField';
import { fieldErrorsFrom, formErrorFrom } from '../../lib/apiErrors';
import {
  MAX_PERCENT,
  MIN_ACTUAL_COST,
  MIN_BUDGET,
  MIN_PERCENT,
  MONEY_STEP,
  NAME_MAX_LENGTH,
  PERCENT_STEP,
} from '../../lib/limits';

interface ActivityFormProps {
  projectId: number;
  activity?: Activity;
  onSaved: () => void;
  onCancel: () => void;
}

type ActivityFormValues = ActivityPayload;

const EMPTY_VALUES: ActivityFormValues = {
  name: '',
  budget_at_completion: '',
  planned_percent: '',
  actual_percent: '',
  actual_cost: '',
};

function valuesFrom(activity: Activity | undefined): ActivityFormValues {
  if (!activity) {
    return EMPTY_VALUES;
  }
  return {
    name: activity.name,
    budget_at_completion: activity.budget_at_completion,
    planned_percent: activity.planned_percent,
    actual_percent: activity.actual_percent,
    actual_cost: activity.actual_cost,
  };
}

/** Values are kept and sent as the strings typed by the user, so no precision is lost. */
export function ActivityForm({ projectId, activity, onSaved, onCancel }: ActivityFormProps) {
  const [values, setValues] = useState<ActivityFormValues>(() => valuesFrom(activity));
  const saveActivity = useSaveActivity(projectId, activity?.id);
  const fieldErrors = fieldErrorsFrom(saveActivity.error);
  const formError = formErrorFrom(saveActivity.error);

  const fieldProps = (field: keyof ActivityFormValues) => ({
    value: values[field],
    onChange: (event: { target: { value: string } }) =>
      setValues((current) => ({ ...current, [field]: event.target.value })),
    error: fieldErrors[field],
    required: true,
  });

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    saveActivity.mutate(values, { onSuccess: onSaved });
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <FormField label="Nombre" maxLength={NAME_MAX_LENGTH} {...fieldProps('name')} />
      <FormField
        label="Presupuesto total (BAC)"
        type="number"
        inputMode="decimal"
        min={MIN_BUDGET}
        step={MONEY_STEP}
        hint="Mayor que 0"
        {...fieldProps('budget_at_completion')}
      />
      <div className="form-row">
        <FormField
          label="% planificado"
          type="number"
          inputMode="decimal"
          min={MIN_PERCENT}
          max={MAX_PERCENT}
          step={PERCENT_STEP}
          hint="Avance esperado a la fecha de corte (0–100)"
          {...fieldProps('planned_percent')}
        />
        <FormField
          label="% real"
          type="number"
          inputMode="decimal"
          min={MIN_PERCENT}
          max={MAX_PERCENT}
          step={PERCENT_STEP}
          hint="Avance completado (0–100)"
          {...fieldProps('actual_percent')}
        />
      </div>
      <FormField
        label="Costo real (AC)"
        type="number"
        inputMode="decimal"
        min={MIN_ACTUAL_COST}
        step={MONEY_STEP}
        hint="Gastado hasta la fecha de corte (0 o más)"
        {...fieldProps('actual_cost')}
      />
      {formError && <AlertMessage text={formError} />}
      <FormActions
        submitLabel="Guardar actividad"
        isSaving={saveActivity.isPending}
        onCancel={onCancel}
      />
    </form>
  );
}
