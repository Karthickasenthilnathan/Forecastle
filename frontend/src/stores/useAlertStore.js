import { create } from 'zustand'
import { getAlerts, markAlertRead } from '../api/alerts'

export const useAlertStore = create((set, get) => ({
  alerts: [],
  fetchAlerts: async () => {
    try {
      const data = await getAlerts(true)
      set({ alerts: data.alerts || [] })
    } catch {
      set({ alerts: [] })
    }
  },
  dismissAlert: async (alertId) => {
    await markAlertRead(alertId)
    set({ alerts: get().alerts.filter((alert) => alert.id !== alertId) })
  },
}))
