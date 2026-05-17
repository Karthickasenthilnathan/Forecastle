import { useEffect, useMemo } from 'react'
import AccuracyGauge from '../components/charts/AccuracyGauge'
import ForecastChart from '../components/charts/ForecastChart'
import SignalContribution from '../components/charts/SignalContribution'
import AlertCard from '../components/cards/AlertCard'
import ExplanationCard from '../components/cards/ExplanationCard'
import ForecastSummaryCard from '../components/cards/ForecastSummaryCard'
import OverrideSlider from '../components/controls/OverrideSlider'
import PageShell from '../components/layout/PageShell'
import LoadingSpinner from '../components/shared/LoadingSpinner'
import { useAlertStore } from '../stores/useAlertStore'
import { useForecastStore } from '../stores/useForecastStore'
import { useProductStore } from '../stores/useProductStore'
import { useSignalStore } from '../stores/useSignalStore'

export default function Dashboard({ navItems }) {
  const {
    products,
    selectedProductId,
    setSelectedProduct,
    fetchProducts,
    isLoading: productsLoading,
    apiUnavailable: productsApiUnavailable,
  } = useProductStore()
  const {
    forecast,
    horizon,
    setHorizon,
    fetchForecast,
    generateForecast,
    isLoading: forecastLoading,
    isGenerating,
    apiUnavailable: forecastApiUnavailable,
    error: forecastError,
  } = useForecastStore()
  const { health, fetchSignals } = useSignalStore()
  const { alerts, fetchAlerts, dismissAlert } = useAlertStore()

  useEffect(() => {
    fetchProducts()
    fetchAlerts()
  }, [fetchAlerts, fetchProducts])

  useEffect(() => {
    if (selectedProductId) {
      fetchForecast(selectedProductId)
      fetchSignals(selectedProductId)
    }
  }, [fetchForecast, fetchSignals, horizon, selectedProductId])

  const selectedProduct = useMemo(
    () => products.find((product) => product.id === selectedProductId),
    [products, selectedProductId],
  )

  const headerProps = {
    products,
    selectedProductId,
    onProductChange: setSelectedProduct,
    horizon,
    onHorizonChange: setHorizon,
    onGenerate: () => generateForecast(selectedProductId),
    isGenerating,
    apiUnavailable: productsApiUnavailable || forecastApiUnavailable,
  }

  return (
    <PageShell navItems={navItems} health={health} headerProps={headerProps}>
      <section className="product-strip">
        <div>
          <span>{selectedProduct?.category || 'Manufacturing'}</span>
          <strong>{selectedProduct?.name || 'Loading product'}</strong>
          <small>{selectedProduct?.sku || 'SKU'} · {selectedProduct?.unit || 'units'}</small>
        </div>
        <div className="model-chip">
          <span />
          Prophet + XGBoost
        </div>
      </section>

      {productsLoading || forecastLoading ? (
        <div className="loading-surface">
          <LoadingSpinner />
          <span>Loading forecast workspace</span>
        </div>
      ) : !selectedProductId || !forecast ? (
        <div className="loading-surface">
          <strong>No API forecast data loaded</strong>
          <span>{forecastError || 'Run the backend seed script, then refresh this page.'}</span>
        </div>
      ) : (
        <>
          <ForecastSummaryCard forecast={forecast} horizon={horizon} />

          <section className="dashboard-grid">
            <div className="primary-column">
              <ForecastChart predictions={forecast?.predictions || []} />
              <div className="two-column">
                <ExplanationCard explanation={forecast?.explanation} />
                <SignalContribution contributions={forecast?.signal_contributions} />
              </div>
            </div>

            <aside className="side-column">
              <AccuracyGauge value={forecast?.accuracy || forecast?.confidence} />
              <OverrideSlider forecast={forecast} />
              <AlertCard alerts={alerts} onDismiss={dismissAlert} />
            </aside>
          </section>
        </>
      )}
    </PageShell>
  )
}
