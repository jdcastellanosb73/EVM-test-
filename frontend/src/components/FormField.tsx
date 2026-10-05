import { useId, type InputHTMLAttributes } from 'react';

interface FormFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  hint?: string;
  error?: string | undefined;
}

export function FormField({ label, hint, error, ...inputProps }: FormFieldProps) {
  const inputId = useId();
  const describedBy = `${inputId}-description`;
  return (
    <div className="form-field">
      <label htmlFor={inputId}>{label}</label>
      <input
        id={inputId}
        aria-invalid={error !== undefined}
        aria-describedby={describedBy}
        {...inputProps}
      />
      <small id={describedBy} className={error === undefined ? 'form-hint' : 'form-error'}>
        {error ?? hint}
      </small>
    </div>
  );
}
