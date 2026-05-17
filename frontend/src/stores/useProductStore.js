import { create } from 'zustand'
import { getProducts, createProduct as apiCreateProduct } from '../api/products'
import { unwrapAxiosError } from '../api/client'

export const useProductStore = create((set, get) => ({
  products: [],
  selectedProductId: null,
  isLoading: false,
  error: null,
  apiUnavailable: false,
  fetchProducts: async () => {
    set({ isLoading: true, error: null })
    try {
      const products = await getProducts()
      set({
        products,
        selectedProductId: get().selectedProductId || products[0]?.id || null,
        apiUnavailable: false,
        isLoading: false,
      })
    } catch (error) {
      set({
        products: [],
        selectedProductId: null,
        apiUnavailable: true,
        error: unwrapAxiosError(error),
        isLoading: false,
      })
    }
  },
  setSelectedProduct: (selectedProductId) => set({ selectedProductId }),
  createProduct: async (payload) => {
    const newProduct = await apiCreateProduct(payload)
    await get().fetchProducts()
    return newProduct
  },
}))
