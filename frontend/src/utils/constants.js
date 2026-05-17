export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

export const HORIZONS = [2, 4, 8]

export const SIGNAL_META = {
  social: { label: 'Social demand', color: '#2dd4bf' },
  weather: { label: 'Weather pressure', color: '#60a5fa' },
  news: { label: 'News events', color: '#f59e0b' },
  supplier: { label: 'Supplier lead time', color: '#f43f5e' },
}
