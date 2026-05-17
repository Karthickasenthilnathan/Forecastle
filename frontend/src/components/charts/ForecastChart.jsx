import {
  Area,
  CartesianGrid,
  ComposedChart,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { formatCompact, formatDate, formatNumber } from '../../utils/formatters'

function normalizePoint(point) {
  const qty = Number(point.qty ?? point.predicted_qty ?? point.predictedQty ?? point.yhat ?? 0)
  const lower = Number(point.lower ?? point.lower_bound ?? point.yhat_lower ?? qty * 0.88)
  const upper = Number(point.upper ?? point.upper_bound ?? point.yhat_upper ?? qty * 1.12)
  return {
    date: point.date || point.forecast_date,
    demand: qty,
    lower,
    upper,
    band: Math.max(upper - lower, 0),
  }
}

export default function ForecastChart({ predictions = [] }) {
  const data = predictions.map(normalizePoint)

  return (
    <section className="panel chart-panel">
      <div className="panel-heading">
        <div>
          <p>Forecast curve</p>
          <h2>Predicted demand with confidence band</h2>
        </div>
      </div>

      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data} margin={{ top: 16, right: 14, left: -16, bottom: 0 }}>
            <defs>
              <linearGradient id="forecastBand" x1="0" x2="0" y1="0" y2="1">
                <stop offset="0%" stopColor="#38bdf8" stopOpacity={0.28} />
                <stop offset="100%" stopColor="#38bdf8" stopOpacity={0.03} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="#26313b" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="date" tickFormatter={formatDate} minTickGap={24} tickLine={false} axisLine={false} />
            <YAxis tickFormatter={formatCompact} tickLine={false} axisLine={false} width={56} />
            <Tooltip
              contentStyle={{
                background: '#0f1720',
                border: '1px solid #26313b',
                borderRadius: 8,
                color: '#e5edf5',
              }}
              formatter={(value, name) => [formatNumber(value), name === 'demand' ? 'Demand' : name]}
              labelFormatter={formatDate}
            />
            <Area dataKey="lower" stackId="band" stroke="none" fill="transparent" isAnimationActive />
            <Area dataKey="band" stackId="band" stroke="none" fill="url(#forecastBand)" isAnimationActive />
            <Line
              type="monotone"
              dataKey="demand"
              stroke="#22c55e"
              strokeWidth={3}
              dot={false}
              activeDot={{ r: 5, fill: '#22c55e' }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}
