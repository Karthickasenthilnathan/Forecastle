import { formatPercent } from '../../utils/formatters'

export default function AccuracyGauge({ value = 0.84 }) {
  const normalized = Number(value || 0) > 1 ? Number(value) / 100 : Number(value || 0)
  const angle = Math.min(Math.max(normalized, 0), 1) * 360

  return (
    <section className="panel gauge-panel">
      <div className="gauge" style={{ '--gauge-angle': `${angle}deg` }}>
        <div>
          <strong>{formatPercent(normalized)}</strong>
          <span>accuracy</span>
        </div>
      </div>
      <p>Rolling model confidence across the current horizon.</p>
    </section>
  )
}
