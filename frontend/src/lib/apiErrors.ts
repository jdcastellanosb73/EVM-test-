import { ApiError } from '../api/client';

const BODY_FIELD_PREFIX = 'body.';
const NAME_TAKEN_CODES = new Set(['PROJECT_NAME_TAKEN', 'ACTIVITY_NAME_TAKEN']);
const NAME_FIELD = 'name';
const CHECK_FIELDS_MESSAGE = 'Revisa los campos marcados.';
const NETWORK_ERROR_MESSAGE = 'No se pudo conectar con el servidor.';

/** User-facing text for the API's stable error codes; unknown codes keep the API message. */
const MESSAGES_BY_CODE: Record<string, string> = {
  PROJECT_NOT_FOUND: 'El proyecto no existe o fue eliminado.',
  ACTIVITY_NOT_FOUND: 'La actividad no existe o fue eliminada.',
  PROJECT_NAME_TAKEN: 'Ya existe un proyecto con ese nombre.',
  ACTIVITY_NAME_TAKEN: 'Este proyecto ya tiene una actividad con ese nombre.',
};

export function userMessageFor(error: Error): string {
  if (!(error instanceof ApiError)) {
    return NETWORK_ERROR_MESSAGE;
  }
  return MESSAGES_BY_CODE[error.body.code] ?? error.message;
}

/** Maps an API error to the form field it concerns, so it is shown next to that input. */
export function fieldErrorsFrom(error: Error | null): Record<string, string> {
  if (!(error instanceof ApiError)) {
    return {};
  }
  if (NAME_TAKEN_CODES.has(error.body.code)) {
    return { [NAME_FIELD]: userMessageFor(error) };
  }
  const errors: Record<string, string> = {};
  for (const detail of error.body.details) {
    if (detail.field?.startsWith(BODY_FIELD_PREFIX)) {
      errors[detail.field.slice(BODY_FIELD_PREFIX.length)] = detail.message;
    }
  }
  return errors;
}

/** Message for errors that do not belong to a single field. */
export function formErrorFrom(error: Error | null): string | null {
  if (error === null) {
    return null;
  }
  return Object.keys(fieldErrorsFrom(error)).length > 0
    ? CHECK_FIELDS_MESSAGE
    : userMessageFor(error);
}
