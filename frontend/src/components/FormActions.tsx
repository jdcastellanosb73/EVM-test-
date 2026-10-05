const CANCEL_LABEL = 'Cancelar';
const SAVING_LABEL = 'Guardando…';

interface FormActionsProps {
  submitLabel: string;
  isSaving: boolean;
  onCancel: () => void;
}

export function FormActions({ submitLabel, isSaving, onCancel }: FormActionsProps) {
  return (
    <div className="form-actions">
      <button type="button" className="button-secondary" onClick={onCancel}>
        {CANCEL_LABEL}
      </button>
      <button type="submit" className="button-primary" disabled={isSaving}>
        {isSaving ? SAVING_LABEL : submitLabel}
      </button>
    </div>
  );
}
