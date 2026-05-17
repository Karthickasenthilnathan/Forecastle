import { SIGNAL_META } from '../../utils/constants'
import { formatPercent } from '../../utils/formatters'

export default function SignalContribution({ contributions = {} }) {
  const entries = Object.entries(contributions)
  const total = entries.reduce((sum, [, value]) => sum + Math.abs(Number(value || 0)), 0) || 1

  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <p>External drivers</p>
          <h2>Signal contribution</h2>
        </div>
      </div>

      <div className="contribution-list">
        {entries.map(([source, value]) => {
          const meta = SIGNAL_META[source] || { label: source, color: '#94a3b8' }
          const width = `${Math.max((Math.abs(value) / total) * 100, 8)}%`
          return (
            <div className="contribution-row" key={source}>
              <div className="row-label">
                <span style={{ background: meta.color }} />
                <strong>{meta.label}</strong>
                <em>{Number(value) >= 0 ? '+' : ''}{formatPercent(value)}</em>
              </div>
              <div className="bar-track">
                <span className={Number(value) >= 0 ? 'positive' : 'negative'} style={{ width, background: meta.color }} />
              </div>
            </div>
          )
        })}
      </div>
    </section>
  )
}
