import { useState, type FormEvent } from 'react';
import { useSaveProject } from '../../api/queries';
import type { Project, ProjectPayload } from '../../api/types';
import { FormField } from '../../components/FormField';
import { fieldErrorsFrom, formErrorFrom } from '../../lib/apiErrors';
import { DESCRIPTION_MAX_LENGTH, NAME_MAX_LENGTH } from '../../lib/limits';

interface ProjectFormProps {
  project?: Pick<Project, 'id' | 'name' | 'description' | 'cutoff_date'>;
  onSaved: (project: Project) => void;
  onCancel: () => void;
}

interface ProjectFormValues {
  name: string;
  description: string;
  cutoffDate: string;
}

function toPayload(values: ProjectFormValues): ProjectPayload {
  return {
    name: values.name,
    description: values.description.trim() === '' ? null : values.description,
    cutoff_date: values.cutoffDate === '' ? null : values.cutoffDate,
  };
}

export function ProjectForm({ project, onSaved, onCancel }: ProjectFormProps) {
  const [values, setValues] = useState<ProjectFormValues>({
    name: project?.name ?? '',
    description: project?.description ?? '',
    cutoffDate: project?.cutoff_date ?? '',
  });
  const saveProject = useSaveProject(project?.id);
  const fieldErrors = fieldErrorsFrom(saveProject.error);
  const formError = formErrorFrom(saveProject.error);

  const update = (field: keyof ProjectFormValues) => (value: string) =>
    setValues((current) => ({ ...current, [field]: value }));

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    saveProject.mutate(toPayload(values), { onSuccess: onSaved });
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <FormField
        label="Nombre"
        required
        maxLength={NAME_MAX_LENGTH}
        value={values.name}
        onChange={(event) => update('name')(event.target.value)}
        error={fieldErrors['name']}
      />
      <FormField
        label="Descripción"
        maxLength={DESCRIPTION_MAX_LENGTH}
        value={values.description}
        onChange={(event) => update('description')(event.target.value)}
        error={fieldErrors['description']}
      />
      <FormField
        label="Fecha de corte"
        type="date"
        hint="Fecha a la que se refieren los porcentajes de avance"
        value={values.cutoffDate}
        onChange={(event) => update('cutoffDate')(event.target.value)}
        error={fieldErrors['cutoff_date']}
      />
      {formError && (
        <p className="feedback feedback-error" role="alert">
          {formError}
        </p>
      )}
      <div className="form-actions">
        <button type="button" className="button-secondary" onClick={onCancel}>
          Cancelar
        </button>
        <button type="submit" className="button-primary" disabled={saveProject.isPending}>
          {saveProject.isPending ? 'Guardando…' : 'Guardar proyecto'}
        </button>
      </div>
    </form>
  );
}
