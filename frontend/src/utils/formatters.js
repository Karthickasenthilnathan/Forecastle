export const numberFormatter = new Intl.NumberFormat('en-US', {
  maximumFractionDigits: 0,
})

export const compactFormatter = new Intl.NumberFormat('en-US', {
  notation: 'compact',
  maximumFractionDigits: 1,
})

export function formatNumber(value) {
  return numberFormatter.format(Number(value || 0))
}

export function formatCompact(value) {
  return compactFormatter.format(Number(value || 0))
}

export function formatPercent(value) {
  const normalized = Number(value || 0)
  const pct = normalized <= 1 ? normalized * 100 : normalized
  return `${Math.round(pct)}%`
}

export function formatDate(value) {
  if (!value) return 'Today'
  return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric' }).format(new Date(value))
}
