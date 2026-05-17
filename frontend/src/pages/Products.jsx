import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { PlusIcon, CubeIcon, ArrowRightIcon, XMarkIcon } from '@heroicons/react/24/outline'
import { motion, AnimatePresence } from 'framer-motion'
import PageShell from '../components/layout/PageShell'
import LoadingSpinner from '../components/shared/LoadingSpinner'
import { useProductStore } from '../stores/useProductStore'
import { useSignalStore } from '../stores/useSignalStore'

const CATEGORIES = ['Electronics', 'Apparel', 'Food', 'Furniture', 'Sports', 'Healthcare', 'Automotive']
const UNITS = ['units', 'cases', 'kits', 'packs', 'kg', 'litres']

const emptyForm = { name: '', sku: '', category: '', unit: 'units' }

export default function Products({ navItems }) {
  const { products, isLoading, apiUnavailable, fetchProducts, createProduct, setSelectedProduct } = useProductStore()
  const { health } = useSignalStore()
  const navigate = useNavigate()

  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(emptyForm)
  const [formError, setFormError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [successMsg, setSuccessMsg] = useState('')

  useEffect(() => {
    fetchProducts()
  }, [fetchProducts])

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
    setFormError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.name.trim() || !form.sku.trim()) {
      setFormError('Product name and SKU are required.')
      return
    }
    setSubmitting(true)
    setFormError('')
    try {
      const created = await createProduct({
        name: form.name.trim(),
        sku: form.sku.trim(),
        category: form.category || null,
        unit: form.unit || 'units',
      })
      setForm(emptyForm)
      setShowForm(false)
      setSuccessMsg(`"${created.name}" added successfully!`)
      setTimeout(() => setSuccessMsg(''), 4000)
    } catch (err) {
      setFormError(err?.response?.data?.detail || 'Failed to create product.')
    } finally {
      setSubmitting(false)
    }
  }

  const handleProductClick = (productId) => {
    setSelectedProduct(productId)
    navigate('/')
  }

  return (
    <PageShell navItems={navItems} health={health} title="Product catalogue" subtitle="Manage tracked products">
      <AnimatePresence>
        {successMsg && (
          <motion.div
            className="success-banner"
            initial={{ opacity: 0, y: -12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
          >
            {successMsg}
          </motion.div>
        )}
      </AnimatePresence>

      <div className="page-actions">
        <button className="primary-action" type="button" onClick={() => setShowForm(!showForm)}>
          {showForm ? <XMarkIcon /> : <PlusIcon />}
          <span>{showForm ? 'Cancel' : 'Add product'}</span>
        </button>
      </div>

      <AnimatePresence>
        {showForm && (
          <motion.form
            className="panel add-product-form"
            onSubmit={handleSubmit}
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            style={{ overflow: 'hidden' }}
          >
            <div className="panel-heading">
              <div>
                <p>New product</p>
                <h2>Add to catalogue</h2>
              </div>
            </div>

            <div className="form-grid">
              <label className="form-field">
                <span>Product name *</span>
                <input type="text" name="name" placeholder="e.g. Smart Thermostat" value={form.name} onChange={handleChange} />
              </label>
              <label className="form-field">
                <span>SKU *</span>
                <input type="text" name="sku" placeholder="e.g. P006" value={form.sku} onChange={handleChange} />
              </label>
              <label className="form-field">
                <span>Category</span>
                <select name="category" value={form.category} onChange={handleChange}>
                  <option value="">Select category</option>
                  {CATEGORIES.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </label>
              <label className="form-field">
                <span>Unit</span>
                <select name="unit" value={form.unit} onChange={handleChange}>
                  {UNITS.map((u) => (
                    <option key={u} value={u}>{u}</option>
                  ))}
                </select>
              </label>
            </div>

            {formError && <p className="form-error">{formError}</p>}

            <div className="form-actions">
              <button className="primary-action" type="submit" disabled={submitting}>
                {submitting ? 'Creating…' : 'Create product'}
              </button>
            </div>
          </motion.form>
        )}
      </AnimatePresence>

      {isLoading ? (
        <div className="loading-surface">
          <LoadingSpinner />
          <span>Loading products</span>
        </div>
      ) : apiUnavailable ? (
        <div className="loading-surface">
          <strong>API unavailable</strong>
          <span>Start the backend server to manage products.</span>
        </div>
      ) : products.length === 0 ? (
        <div className="loading-surface">
          <CubeIcon style={{ width: '2.5rem', height: '2.5rem' }} />
          <strong>No products yet</strong>
          <span>Click "Add product" above to create your first product.</span>
        </div>
      ) : (
        <div className="product-grid">
          {products.map((product) => (
            <motion.button
              className="product-card panel"
              key={product.id}
              type="button"
              onClick={() => handleProductClick(product.id)}
              whileHover={{ scale: 1.015 }}
              whileTap={{ scale: 0.995 }}
            >
              <div className="product-card-header">
                <span className="product-category-badge">{product.category || 'General'}</span>
                <ArrowRightIcon />
              </div>
              <strong className="product-card-name">{product.name}</strong>
              <div className="product-card-meta">
                <span>{product.sku}</span>
                <span>·</span>
                <span>{product.unit}</span>
              </div>
              {product.latest_forecast && (
                <div className="product-card-forecast">
                  <span>Latest forecast</span>
                  <strong>{product.latest_forecast.predicted_qty} {product.unit}</strong>
                </div>
              )}
            </motion.button>
          ))}
        </div>
      )}
    </PageShell>
  )
}
