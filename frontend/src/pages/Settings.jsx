import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import {
  Cog6ToothIcon,
  BellAlertIcon,
  ServerIcon,
  InformationCircleIcon,
  CheckCircleIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline'
import PageShell from '../components/layout/PageShell'
import { useProductStore } from '../stores/useProductStore'
import { useSignalStore } from '../stores/useSignalStore'
import { useAlertStore } from '../stores/useAlertStore'
import { apiClient } from '../api/client'
import { HORIZONS, SIGNAL_META } from '../utils/constants'

const METRICS = ['deviation_pct', 'demand_spike', 'signal_drop']
const DIRECTIONS = ['above', 'below']

const emptyAlert = { product_id: '', metric: 'deviation_pct', threshold: 10, direction: 'above' }

export default function Settings({ navItems }) {
  const { products, fetchProducts, apiUnavailable } = useProductStore()
  const { health } = useSignalStore()
  const { alerts, fetchAlerts } = useAlertStore()

  const [alertForm, setAlertForm] = useState(emptyAlert)
  const [alertSubmitting, setAlertSubmitting] = useState(false)
  const [alertSuccess, setAlertSuccess] = useState('')
  const [alertError, setAlertError] = useState('')

  useEffect(() => {
    fetchProducts()
    fetchAlerts()
  }, [fetchProducts, fetchAlerts])

  useEffect(() => {
    if (products.length > 0 && !alertForm.product_id) {
      setAlertForm((prev) => ({ ...prev, product_id: products[0].id }))
    }
  }, [products, alertForm.product_id])

  const handleAlertChange = (e) => {
    const value = e.target.type === 'number' ? Number(e.target.value) : e.target.value
    setAlertForm({ ...alertForm, [e.target.name]: value })
    setAlertError('')
  }

  const handleAlertSubmit = async (e) => {
    e.preventDefault()
    if (!alertForm.product_id || !alertForm.threshold) {
      setAlertError('All fields are required.')
      return
    }
    setAlertSubmitting(true)
    setAlertError('')
    try {
      await apiClient.post('/alerts/config', {
        product_id: Number(alertForm.product_id),
        metric: alertForm.metric,
        threshold: Number(alertForm.threshold),
        direction: alertForm.direction,
      })
      setAlertSuccess('Alert rule created!')
      setAlertForm({ ...emptyAlert, product_id: alertForm.product_id })
      fetchAlerts()
      setTimeout(() => setAlertSuccess(''), 4000)
    } catch (err) {
      setAlertError(err?.response?.data?.detail || 'Failed to create alert rule.')
    } finally {
      setAlertSubmitting(false)
    }
  }

  return (
    <PageShell navItems={navItems} health={health} title="Settings" subtitle="System configuration">
      <div className="settings-grid">

        {/* Alert Configuration */}
        <motion.div
          className="panel settings-panel"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="panel-heading">
            <div>
              <p>Alert engine</p>
              <h2><BellAlertIcon /> Create alert rule</h2>
            </div>
          </div>

          <form className="settings-form" onSubmit={handleAlertSubmit}>
            <label className="form-field">
              <span>Product</span>
              <select name="product_id" value={alertForm.product_id} onChange={handleAlertChange}>
                {products.map((p) => (
                  <option key={p.id} value={p.id}>{p.name}</option>
                ))}
              </select>
            </label>
            <label className="form-field">
              <span>Metric</span>
              <select name="metric" value={alertForm.metric} onChange={handleAlertChange}>
                {METRICS.map((m) => (
                  <option key={m} value={m}>{m.replace(/_/g, ' ')}</option>
                ))}
              </select>
            </label>
            <label className="form-field">
              <span>Threshold</span>
              <input type="number" name="threshold" min="0" step="0.1" value={alertForm.threshold} onChange={handleAlertChange} />
            </label>
            <label className="form-field">
              <span>Direction</span>
              <select name="direction" value={alertForm.direction} onChange={handleAlertChange}>
                {DIRECTIONS.map((d) => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </label>

            {alertError && <p className="form-error">{alertError}</p>}
            {alertSuccess && <p className="form-success">{alertSuccess}</p>}

            <button className="primary-action" type="submit" disabled={alertSubmitting}>
              {alertSubmitting ? 'Creating…' : 'Create alert rule'}
            </button>
          </form>
        </motion.div>

        {/* Active Alerts */}
        <motion.div
          className="panel settings-panel"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05 }}
        >
          <div className="panel-heading">
            <div>
              <p>Active alerts</p>
              <h2><BellAlertIcon /> {alerts.length} unread</h2>
            </div>
          </div>
          {alerts.length === 0 ? (
            <div className="quiet-state">
              <span>No unread alerts</span>
            </div>
          ) : (
            <div className="alert-list">
              {alerts.map((a) => (
                <div className="alert-card" key={a.id}>
                  <div>
                    <strong>Alert #{a.id}</strong>
                    <span>{a.message}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </motion.div>

        {/* Connection Status */}
        <motion.div
          className="panel settings-panel"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <div className="panel-heading">
            <div>
              <p>Infrastructure</p>
              <h2><ServerIcon /> Connection status</h2>
            </div>
          </div>
          <div className="settings-status-list">
            <div className="settings-status-row">
              <span>API Server</span>
              {apiUnavailable
                ? <span className="settings-badge down"><XCircleIcon /> Offline</span>
                : <span className="settings-badge up"><CheckCircleIcon /> Connected</span>
              }
            </div>
            <div className="settings-status-row">
              <span>Signal Pipeline</span>
              <span className={`settings-badge ${health?.overall === 'healthy' ? 'up' : 'down'}`}>
                {health?.overall === 'healthy' ? <><CheckCircleIcon /> Healthy</> : <><XCircleIcon /> Degraded</>}
              </span>
            </div>
            <div className="settings-status-row">
              <span>Products tracked</span>
              <strong>{products.length}</strong>
            </div>
            <div className="settings-status-row">
              <span>Signal sources</span>
              <strong>{Object.keys(SIGNAL_META).length}</strong>
            </div>
          </div>
        </motion.div>

        {/* System Info */}
        <motion.div
          className="panel settings-panel"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
        >
          <div className="panel-heading">
            <div>
              <p>System</p>
              <h2><InformationCircleIcon /> Platform info</h2>
            </div>
          </div>
          <div className="settings-info-list">
            <div className="settings-info-row">
              <span>Forecast model</span>
              <strong>Prophet + XGBoost (hybrid)</strong>
            </div>
            <div className="settings-info-row">
              <span>Available horizons</span>
              <strong>{HORIZONS.map((h) => `${h}W`).join(' · ')}</strong>
            </div>
            <div className="settings-info-row">
              <span>Signal sources</span>
              <strong>{Object.values(SIGNAL_META).map((m) => m.label).join(', ')}</strong>
            </div>
            <div className="settings-info-row">
              <span>Version</span>
              <strong>Forecastle v0.1.0-alpha</strong>
            </div>
          </div>
        </motion.div>
      </div>
    </PageShell>
  )
}
