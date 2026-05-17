import { XMarkIcon } from '@heroicons/react/24/outline'
import { formatDate, formatPercent } from '../../utils/formatters'

export default function AlertCard({ alerts = [], onDismiss }) {
  return (
    <section className="panel alerts-panel">
      <div className="panel-heading">
        <div>
          <p>Threshold monitor</p>
          <h2>Active alerts</h2>
        </div>
      </div>

      <div className="alert-list">
        {alerts.length ? (
          alerts.map((alert) => (
            <article className="alert-card" key={alert.id}>
              <div>
                <strong>{alert.message}</strong>
                <span>
                  {formatPercent(alert.metric_value)} · {formatDate(alert.triggered_at)}
                </span>
              </div>
              <button type="button" aria-label="Dismiss alert" onClick={() => onDismiss(alert.id)}>
                <XMarkIcon />
              </button>
            </article>
          ))
        ) : (
          <div className="quiet-state">No unread alerts.</div>
        )}
      </div>
    </section>
  )
}
