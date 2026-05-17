import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowPathIcon, SignalIcon, CheckCircleIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'
import PageShell from '../components/layout/PageShell'
import LoadingSpinner from '../components/shared/LoadingSpinner'
import { useProductStore } from '../stores/useProductStore'
import { useSignalStore } from '../stores/useSignalStore'
import { getSignals, collectSignals } from '../api/signals'
import { SIGNAL_META } from '../utils/constants'

export default function Signals({ navItems }) {
  const { products, fetchProducts } = useProductStore()
  const { health, fetchSignals } = useSignalStore()

  const [selectedPid, setSelectedPid] = useState(null)
  const [signals, setSignals] = useState([])
  const [loadingSignals, setLoadingSignals] = useState(false)
  const [collecting, setCollecting] = useState(false)
  const [collectResult, setCollectResult] = useState('')

  useEffect(() => {
    fetchProducts()
  }, [fetchProducts])

  useEffect(() => {
    if (products.length > 0 && !selectedPid) {
      setSelectedPid(products[0].id)
    }
  }, [products, selectedPid])

  useEffect(() => {
    if (!selectedPid) return
    setLoadingSignals(true)
    fetchSignals(selectedPid)
    getSignals(selectedPid)
      .then((data) => setSignals(data.signals || []))
      .catch(() => setSignals([]))
      .finally(() => setLoadingSignals(false))
  }, [selectedPid, fetchSignals])

  const handleCollect = async () => {
    if (!selectedPid || collecting) return
    setCollecting(true)
    setCollectResult('')
    try {
      const result = await collectSignals(selectedPid)
      setCollectResult(`Collected from ${result.sources_collected} sources`)
      // Refresh signals
      const data = await getSignals(selectedPid)
      setSignals(data.signals || [])
      fetchSignals(selectedPid)
      setTimeout(() => setCollectResult(''), 4000)
    } catch {
      setCollectResult('Collection failed')
      setTimeout(() => setCollectResult(''), 4000)
    } finally {
      setCollecting(false)
    }
  }

  const groupedSignals = signals.reduce((acc, s) => {
    if (!acc[s.source]) acc[s.source] = []
    acc[s.source].push(s)
    return acc
  }, {})

  return (
    <PageShell navItems={navItems} health={health} title="Signal intelligence" subtitle="External demand signals">

      {/* Health overview cards */}
      <section className="signal-health-grid">
        {(health?.sources || []).map((source) => {
          const meta = SIGNAL_META[source.source] || { label: source.source, color: '#8fa1b3' }
          const isHealthy = source.status === 'healthy'
          return (
            <motion.div
              className="panel signal-health-card"
              key={source.source}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="signal-health-header">
                <span className="signal-source-dot" style={{ background: meta.color }} />
                <strong>{meta.label}</strong>
                {isHealthy
                  ? <CheckCircleIcon className="signal-status-icon healthy" />
                  : <ExclamationTriangleIcon className="signal-status-icon degraded" />
                }
              </div>
              <span className="signal-health-status">{isHealthy ? 'Operational' : 'Degraded'}</span>
              {source.latest_collected && (
                <small className="signal-health-time">Last collected: {new Date(source.latest_collected).toLocaleString()}</small>
              )}
            </motion.div>
          )
        })}
        {(!health?.sources || health.sources.length === 0) && (
          <>
            {Object.entries(SIGNAL_META).map(([key, meta]) => (
              <div className="panel signal-health-card" key={key}>
                <div className="signal-health-header">
                  <span className="signal-source-dot" style={{ background: meta.color }} />
                  <strong>{meta.label}</strong>
                  <SignalIcon className="signal-status-icon" />
                </div>
                <span className="signal-health-status">Awaiting data</span>
              </div>
            ))}
          </>
        )}
      </section>

      {/* Product selector + collect */}
      <div className="signal-toolbar">
        <div className="select-control">
          <span>Product</span>
          <select value={selectedPid || ''} onChange={(e) => setSelectedPid(Number(e.target.value))}>
            {products.map((p) => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
        </div>
        <button className="primary-action" type="button" onClick={handleCollect} disabled={collecting}>
          <ArrowPathIcon className={collecting ? 'spin' : ''} />
          <span>{collecting ? 'Collecting…' : 'Collect signals'}</span>
        </button>
        {collectResult && <span className="status-pill live">{collectResult}</span>}
      </div>

      {/* Per-product signal breakdown */}
      {loadingSignals ? (
        <div className="loading-surface">
          <LoadingSpinner />
          <span>Loading signals</span>
        </div>
      ) : signals.length === 0 ? (
        <div className="loading-surface">
          <SignalIcon style={{ width: '2.5rem', height: '2.5rem' }} />
          <strong>No signals recorded</strong>
          <span>Click "Collect signals" to pull from external sources.</span>
        </div>
      ) : (
        <div className="signal-source-grid">
          {Object.entries(groupedSignals).map(([source, items]) => {
            const meta = SIGNAL_META[source] || { label: source, color: '#8fa1b3' }
            return (
              <motion.div
                className="panel signal-source-panel"
                key={source}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <div className="panel-heading">
                  <div>
                    <p style={{ color: meta.color }}>{source.toUpperCase()}</p>
                    <h2>{meta.label}</h2>
                  </div>
                </div>
                <div className="signal-items">
                  {items.map((signal) => (
                    <div className="signal-item" key={signal.id}>
                      <div className="signal-item-header">
                        <strong>{signal.signal_name}</strong>
                        <span className={signal.signal_value >= 0 ? 'signal-value positive' : 'signal-value negative'}>
                          {signal.signal_value >= 0 ? '+' : ''}{(signal.signal_value * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="bar-track">
                        <span
                          className={signal.signal_value < 0 ? 'negative' : ''}
                          style={{
                            width: `${Math.min(Math.abs(signal.signal_value) * 500, 100)}%`,
                            background: meta.color,
                          }}
                        />
                      </div>
                      <small className="signal-item-date">{signal.date} · {signal.collected_at ? new Date(signal.collected_at).toLocaleTimeString() : 'N/A'}</small>
                    </div>
                  ))}
                </div>
              </motion.div>
            )
          })}
        </div>
      )}
    </PageShell>
  )
}
