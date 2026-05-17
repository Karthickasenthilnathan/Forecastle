import { LightBulbIcon } from '@heroicons/react/24/outline'

export default function ExplanationCard({ explanation }) {
  return (
    <section className="panel explanation-card">
      <div className="panel-heading">
        <div>
          <p>Forecast rationale</p>
          <h2>Why did the forecast move?</h2>
        </div>
        <LightBulbIcon />
      </div>
      <p>{explanation || 'No explanation is available for this forecast yet.'}</p>
    </section>
  )
}
