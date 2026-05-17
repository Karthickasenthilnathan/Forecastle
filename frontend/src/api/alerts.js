import { apiClient } from './client'

export async function getAlerts(unread = true) {
  const { data } = await apiClient.get('/alerts/', { params: { unread } })
  return data
}

export async function markAlertRead(alertId) {
  await apiClient.put(`/alerts/${alertId}/read`)
}
