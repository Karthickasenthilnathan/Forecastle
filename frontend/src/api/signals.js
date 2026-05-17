import { apiClient } from './client'

export async function getSignals(productId) {
  const { data } = await apiClient.get(`/signals/${productId}`)
  return data
}

export async function getSignalHealth() {
  const { data } = await apiClient.get('/signals/health/status')
  return data
}

export async function collectSignals(productId) {
  const { data } = await apiClient.post('/signals/collect', null, {
    params: { product_id: productId },
  })
  return data
}
