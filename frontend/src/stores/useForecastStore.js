import { create } from 'zustand'
import { generateForecast, getForecast } from '../api/forecasts'
import { unwrapAxiosError } from '../api/client'

function normalizeForecast(data, productId, horizon) {
  if (!data || data.error) {
    throw new Error(data?.error || `No forecast found for product ${productId} at ${horizon}W`)
  }
  if (Array.isArray(data.predictions) && data.predictions.length) return data

  const forecastDate = data.forecast_date || new Date().toISOString().slice(0, 10)
  const qty = Number(data.override_qty || data.predicted_qty || 0)
  return {
    ...data,
    forecast_id: data.id,
    predictions: [
      {
        date: forecastDate,
        qty,
        predicted_qty: qty,
        lower: data.lower_bound,
        upper: data.upper_bound,
        lower_bound: data.lower_bound,
        upper_bound: data.upper_bound,
      },
    ],
    accuracy: data.confidence || 0.82,
  }
}

export const useForecastStore = create((set, get) => ({
  horizon: 4,
  forecast: null,
  isLoading: false,
  isGenerating: false,
  error: null,
  apiUnavailable: false,
  setHorizon: (horizon) => set({ horizon }),
  fetchForecast: async (productId) => {
    const { horizon } = get()
    if (!productId) return
    set({ isLoading: true, error: null })
    try {
      const data = await getForecast(productId, horizon)
      set({
        forecast: normalizeForecast(data, productId, horizon),
        apiUnavailable: false,
        isLoading: false,
      })
    } catch (error) {
      set({
        forecast: null,
        apiUnavailable: true,
        error: unwrapAxiosError(error),
        isLoading: false,
      })
    }
  },
  generateForecast: async (productId) => {
    const { horizon } = get()
    if (!productId) return
    set({ isGenerating: true, error: null })
    try {
      const data = await generateForecast(productId, horizon)
      set({
        forecast: normalizeForecast(data, productId, horizon),
        apiUnavailable: false,
        isGenerating: false,
      })
    } catch (error) {
      set({
        forecast: null,
        apiUnavailable: true,
        error: unwrapAxiosError(error),
        isGenerating: false,
      })
    }
  },
}))
