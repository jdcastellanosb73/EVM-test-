/**
 * Display formatting. Values arrive as decimal strings and are passed to Intl.NumberFormat
 * as strings, never converted to number, so large amounts keep their exact digits.
 */

import type { DecimalString } from '../api/types';

const LOCALE = 'es-CO';
const MONEY_DECIMALS = 2;
const INDEX_DECIMALS = 4;
const PERCENT_MAX_DECIMALS = 2;
export const MISSING_VALUE = '—';

const moneyFormat = new Intl.NumberFormat(LOCALE, {
  minimumFractionDigits: MONEY_DECIMALS,
  maximumFractionDigits: MONEY_DECIMALS,
});
const indexFormat = new Intl.NumberFormat(LOCALE, {
  minimumFractionDigits: INDEX_DECIMALS,
  maximumFractionDigits: INDEX_DECIMALS,
});
const percentFormat = new Intl.NumberFormat(LOCALE, {
  maximumFractionDigits: PERCENT_MAX_DECIMALS,
});
const dateFormat = new Intl.DateTimeFormat(LOCALE, {
  day: 'numeric',
  month: 'short',
  year: 'numeric',
  timeZone: 'UTC',
});

function formatDecimal(format: Intl.NumberFormat, value: DecimalString | null): string {
  return value === null ? MISSING_VALUE : format.format(value as Intl.StringNumericLiteral);
}

export const formatMoney = (value: DecimalString | null) => formatDecimal(moneyFormat, value);

export const formatIndex = (value: DecimalString | null) => formatDecimal(indexFormat, value);

export const formatPercent = (value: DecimalString) => `${formatDecimal(percentFormat, value)} %`;

/** Dates come as ISO "YYYY-MM-DD"; formatted in UTC so the day never shifts. */
export const formatDate = (isoDate: string | null) =>
  isoDate === null ? MISSING_VALUE : dateFormat.format(new Date(isoDate));

/** Sign of a decimal string, read from its text: no float conversion involved. */
export function isNegative(value: DecimalString | null): boolean {
  return value !== null && value.trim().startsWith('-');
}
