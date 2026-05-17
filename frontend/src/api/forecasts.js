import { apiClient } from './client'

export async function getForecast(productId, horizon) {
  const { data } = await apiClient.get(`/forecasts/${productId}`, { params: { horizon } })
  return data
}

export async function generateForecast(productId, horizonWeeks) {
  const { data } = await apiClient.post('/forecasts/generate', null, {
    params: { product_id: productId, horizon_weeks: horizonWeeks },
  })
  return data
}

export async function overrideForecast(forecastId, overrideQty) {
  const { data } = await apiClient.post(`/forecasts/${forecastId}/override`, null, {
    params: { override_qty: overrideQty },
  })
  return data
}
