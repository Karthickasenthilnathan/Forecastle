import { useMemo, useState } from 'react'
import { formatNumber, formatPercent } from '../../utils/formatters'

export default function OverrideSlider({ forecast }) {
  const original = useMemo(() => {
    const first = forecast?.predictions?.[0]
    return Number(forecast?.override_qty || first?.qty || first?.predicted_qty || forecast?.predicted_qty || 500)
  }, [forecast])
  const [value, setValue] = useState(original)
  const impact = original ? (Number(value) - original) / original : 0

  return (
    <section className="panel override-panel">
      <div className="panel-heading">
        <div>
          <p>Manual simulation</p>
          <h2>Override first forecast point</h2>
        </div>
      </div>
      <input
        type="range"
        min={Math.max(Math.round(original * 0.55), 1)}
        max={Math.round(original * 1.55)}
        value={value}
        onChange={(event) => setValue(Number(event.target.value))}
      />
      <div className="override-output">
        <strong>{formatNumber(value)}</strong>
        <span>{impact >= 0 ? '+' : ''}{formatPercent(impact)} capacity impact</span>
      </div>
    </section>
  )
}
