import { describe, expect, it } from 'vitest';
import {
  MISSING_VALUE,
  formatDate,
  formatIndex,
  formatMoney,
  formatPercent,
  isNegative,
} from './format';

describe('formatMoney', () => {
  it('formats the API string with es-CO separators and 2 decimals', () => {
    expect(formatMoney('26666666.67')).toBe('26.666.666,67');
    expect(formatMoney('-4400000.00')).toBe('-4.400.000,00');
  });

  it('keeps every digit of amounts beyond float precision', () => {
    const amount = '12345678901234567.89';

    expect(formatMoney(amount)).toBe('12.345.678.901.234.567,89');
    expect(formatMoney(String(Number(amount)))).not.toBe(formatMoney(amount));
  });

  it('shows a dash for indicators the API could not compute', () => {
    expect(formatMoney(null)).toBe(MISSING_VALUE);
  });
});

describe('formatIndex', () => {
  it('shows the 4 decimals the API sent', () => {
    expect(formatIndex('0.8854')).toBe('0,8854');
    expect(formatIndex('1.0000')).toBe('1,0000');
  });

  it('shows a dash for a not applicable index', () => {
    expect(formatIndex(null)).toBe(MISSING_VALUE);
  });
});

describe('formatPercent', () => {
  it('drops trailing zeros and adds the percent sign', () => {
    expect(formatPercent('60.00')).toBe('60 %');
    expect(formatPercent('45.50')).toBe('45,5 %');
  });
});

describe('formatDate', () => {
  it('formats the cutoff date without shifting the day by time zone', () => {
    expect(formatDate('2026-10-03')).toMatch(/^3\D*oct\D*2026$/);
    expect(formatDate(null)).toBe(MISSING_VALUE);
  });
});

describe('isNegative', () => {
  it('reads the sign from the string', () => {
    expect(isNegative('-0.01')).toBe(true);
    expect(isNegative('0.00')).toBe(false);
    expect(isNegative(null)).toBe(false);
  });
});
