import axios from 'axios'
import { API_BASE_URL } from '../utils/constants'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 8000,
})

export function unwrapAxiosError(error) {
  if (error.response?.data?.detail) return error.response.data.detail
  if (error.response?.data?.error) return error.response.data.error
  return error.message || 'Unable to reach Forecastle API'
}
