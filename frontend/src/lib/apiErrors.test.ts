import { describe, expect, it } from 'vitest';
import { ApiError } from '../api/client';
import { fieldErrorsFrom, formErrorFrom, userMessageFor } from './apiErrors';

const UNPROCESSABLE = 422;
const CONFLICT = 409;
const NOT_FOUND = 404;
const METHOD_NOT_ALLOWED = 405;

describe('fieldErrorsFrom', () => {
  it('maps validation details to the form fields', () => {
    const error = new ApiError(UNPROCESSABLE, {
      code: 'VALIDATION_ERROR',
      message: 'Request validation failed',
      details: [
        { field: 'body.budget_at_completion', message: 'Input should be greater than 0' },
        { field: 'path.project_id', message: 'Input should be a valid integer' },
      ],
    });

    expect(fieldErrorsFrom(error)).toEqual({
      budget_at_completion: 'Input should be greater than 0',
    });
    expect(formErrorFrom(error)).toBe('Revisa los campos marcados.');
  });

  it('shows a taken name next to the name field', () => {
    const error = new ApiError(CONFLICT, {
      code: 'ACTIVITY_NAME_TAKEN',
      message: "An activity named 'Diseño UX' already exists in project 1",
      details: [],
    });

    expect(fieldErrorsFrom(error)).toEqual({
      name: 'Este proyecto ya tiene una actividad con ese nombre.',
    });
  });

  it('shows errors that belong to no field as a form message', () => {
    const notFound = new ApiError(NOT_FOUND, {
      code: 'PROJECT_NOT_FOUND',
      message: 'Project 7 not found',
      details: [],
    });

    expect(fieldErrorsFrom(notFound)).toEqual({});
    expect(formErrorFrom(notFound)).toBe('El proyecto no existe o fue eliminado.');
    expect(formErrorFrom(null)).toBeNull();
  });
});

describe('userMessageFor', () => {
  it('explains network failures without leaking technical details', () => {
    expect(userMessageFor(new Error('Failed to fetch'))).toBe(
      'No se pudo conectar con el servidor.',
    );
  });

  it('falls back to the API message for codes without a translation', () => {
    const error = new ApiError(METHOD_NOT_ALLOWED, {
      code: 'METHOD_NOT_ALLOWED',
      message: 'Method Not Allowed',
      details: [],
    });

    expect(userMessageFor(error)).toBe('Method Not Allowed');
  });
});
