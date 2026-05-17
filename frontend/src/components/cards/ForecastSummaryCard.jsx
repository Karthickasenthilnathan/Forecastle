import { ArrowTrendingUpIcon, ChartPieIcon, ScaleIcon, ShieldCheckIcon } from '@heroicons/react/24/outline'
import { formatNumber, formatPercent } from '../../utils/formatters'

function totalDemand(predictions = [], fallback = 0) {
  if (!predictions.length) return Number(fallback || 0)
  return predictions.reduce((sum, point) => sum + Number(point.qty ?? point.predicted_qty ?? point.yhat ?? 0), 0)
}

export default function ForecastSummaryCard({ forecast, horizon }) {
  const demand = totalDemand(forecast?.predictions, forecast?.predicted_qty)
  const confidence = forecast?.confidence ?? 0.82
  const deviation = 0.074

  const cards = [
    { label: `${horizon} week demand`, value: formatNumber(demand), icon: ChartPieIcon },
    { label: 'Model confidence', value: formatPercent(confidence), icon: ShieldCheckIcon },
    { label: 'Baseline deviation', value: `+${formatPercent(deviation)}`, icon: ArrowTrendingUpIcon },
    { label: 'Planning buffer', value: formatNumber(demand * 0.12), icon: ScaleIcon },
  ]

  return (
    <section className="summary-grid">
      {cards.map((card) => {
        const Icon = card.icon
        return (
          <article className="kpi-card" key={card.label}>
            <Icon />
            <span>{card.label}</span>
            <strong>{card.value}</strong>
          </article>
        )
      })}
    </section>
  )
}
