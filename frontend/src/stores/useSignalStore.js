import { create } from 'zustand'
import { collectSignals, getSignalHealth, getSignals } from '../api/signals'

export const useSignalStore = create((set) => ({
  signals: [],
  health: { overall: 'unknown', sources: [] },
  isLoading: false,
  fetchSignals: async (productId) => {
    if (!productId) return
    set({ isLoading: true })
    try {
      const [signalsData, healthData] = await Promise.all([getSignals(productId), getSignalHealth()])
      set({ signals: signalsData.signals || [], health: healthData, isLoading: false })
    } catch {
      set({ signals: [], health: { overall: 'unknown', sources: [] }, isLoading: false })
    }
  },
  collect: async (productId) => {
    if (!productId) return
    await collectSignals(productId)
  },
}))
