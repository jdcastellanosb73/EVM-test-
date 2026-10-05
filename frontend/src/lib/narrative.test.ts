import { describe, expect, it } from 'vitest';
import type { Indicators, PerformanceIndex } from '../api/types';
import {
  readCostPerformance,
  readEstimateAtCompletion,
  readProjectVerdict,
  readSchedulePerformance,
  readVarianceAtCompletion,
} from './narrative';

/** CPI/SPI as the API returns them; the interpretation text is not what these tests check. */
function index<Status>(value: string | null, status: Status): PerformanceIndex<Status> {
  return { value, status, interpretation: '' };
}

// Consolidated demo project "Portal de clientes", as the API returns it.
const DEMO_PROJECT: Indicators = {
  bac: '34000000.00',
  pv: '21200000.00',
  ev: '17000000.00',
  ac: '19200000.00',
  cv: '-2200000.00',
  sv: '-4200000.00',
  cpi: index('0.8854', 'OVER_BUDGET'),
  spi: index('0.8019', 'BEHIND_SCHEDULE'),
  eac: '38400000.00',
  vac: '-4400000.00',
};

describe('readCostPerformance', () => {
  it('reads a CPI shown as 1,0000 as over budget when the API says so', () => {
    const reading = readCostPerformance(index('1.0000', 'OVER_BUDGET'));

    expect(reading.label).toBe('Sobre presupuesto');
    expect(reading.tone).toBe('bad');
    expect(reading.sentence).toContain('1,0000');
    expect(reading.sentence).toContain('gasta más de lo que avanza');
  });

  it('explains an efficient project', () => {
    const reading = readCostPerformance(index('1.1111', 'UNDER_BUDGET'));

    expect(reading.tone).toBe('good');
    expect(reading.sentence).toBe(
      'Por cada peso gastado se obtienen 1,1111 en trabajo: gasta menos de lo que avanza.',
    );
  });

  it('says why there is no CPI instead of showing a number', () => {
    const reading = readCostPerformance(index(null, 'NOT_APPLICABLE'));

    expect(reading.tone).toBe('neutral');
    expect(reading.sentence).toContain('no hay costo registrado');
  });
});

describe('readSchedulePerformance', () => {
  it('reads an SPI shown as 1,0000 as ahead when the API says so', () => {
    const reading = readSchedulePerformance(index('1.0000', 'AHEAD_OF_SCHEDULE'));

    expect(reading.label).toBe('Adelantado');
    expect(reading.tone).toBe('good');
    expect(reading.sentence).toContain('va por delante del plan');
  });

  it('explains a project behind schedule', () => {
    expect(readSchedulePerformance(DEMO_PROJECT.spi).sentence).toBe(
      'Lleva 0,8019 de avance por cada peso planificado: va por detrás del plan.',
    );
  });
});

describe('readEstimateAtCompletion', () => {
  it('compares the estimate with the budget using the cost status', () => {
    const reading = readEstimateAtCompletion(DEMO_PROJECT);

    expect(reading.tone).toBe('bad');
    expect(reading.label).toBe('Por encima del presupuesto');
    expect(reading.sentence).toBe(
      'Si sigue igual, costará 38.400.000,00 frente a un presupuesto de 34.000.000,00.',
    );
  });

  it('explains a missing estimate', () => {
    const reading = readEstimateAtCompletion({
      ...DEMO_PROJECT,
      cpi: index(null, 'NOT_APPLICABLE'),
      eac: null,
      vac: null,
    });

    expect(reading.tone).toBe('neutral');
    expect(reading.label).toBe('Sin estimación');
  });
});

describe('readVarianceAtCompletion', () => {
  it('says how much money would be missing, without a double negative', () => {
    const reading = readVarianceAtCompletion(DEMO_PROJECT);

    expect(reading.label).toBe('Falta presupuesto');
    expect(reading.sentence).toBe('Al terminar faltarían 4.400.000,00 para cubrir el costo.');
  });

  it('says how much money would be left over', () => {
    const reading = readVarianceAtCompletion({
      ...DEMO_PROJECT,
      cpi: index('1.1111', 'UNDER_BUDGET'),
      eac: '18000000.00',
      vac: '2000000.00',
    });

    expect(reading.tone).toBe('good');
    expect(reading.sentence).toBe('Al terminar sobrarían 2.000.000,00 del presupuesto.');
  });

  it('explains a missing variance', () => {
    const reading = readVarianceAtCompletion({ ...DEMO_PROJECT, eac: null, vac: null });

    expect(reading.tone).toBe('neutral');
    expect(reading.label).toBe('Sin estimación');
  });
});

describe('readEstimateAtCompletion labels', () => {
  it('does not claim "within budget" when the CPI cannot be measured', () => {
    const reading = readEstimateAtCompletion({
      ...DEMO_PROJECT,
      cpi: index(null, 'NOT_APPLICABLE'),
    });

    expect(reading.tone).toBe('neutral');
    expect(reading.label).toBe('Sin estimación');
  });
});

describe('readProjectVerdict', () => {
  it('asks for attention when cost or schedule is bad', () => {
    expect(readProjectVerdict(DEMO_PROJECT)).toBe(
      'Requiere atención: sobre presupuesto y atrasado.',
    );
  });

  it('does not call an empty project "as expected"', () => {
    const verdict = readProjectVerdict({
      ...DEMO_PROJECT,
      cpi: index(null, 'NOT_APPLICABLE'),
      spi: index(null, 'NOT_APPLICABLE'),
    });

    expect(verdict).toContain('Aún sin datos suficientes');
  });

  it('says the project is on track when nothing is bad', () => {
    const verdict = readProjectVerdict({
      ...DEMO_PROJECT,
      cpi: index('1.1111', 'UNDER_BUDGET'),
      spi: index(null, 'NOT_APPLICABLE'),
    });

    expect(verdict).toBe('Va según lo esperado: bajo presupuesto y sin avance planificado.');
  });
});
