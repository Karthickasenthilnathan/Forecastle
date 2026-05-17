import { apiClient } from './client'

export async function getProducts() {
  const { data } = await apiClient.get('/products/')
  return data
}

export async function createProduct(payload) {
  const { data } = await apiClient.post('/products/', payload)
  return data
}
