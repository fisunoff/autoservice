import axios from 'axios'
import router from '@/router'
import {
  getLocalAccessToken,
  getLocalRefreshToken,
  removeUser,
  setUser,
} from '@/api/tokensSrvices.ts'

export const BASE_URL = 'http://localhost:80/api'
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const token = getLocalAccessToken()
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

api.interceptors.response.use(
  (res) => {
    return res
  },
  async (err) => {
    const originalConfig = err.config

    if (err.response && err.response.status === 401 && !originalConfig._retry) {
      originalConfig._retry = true

      try {
        const response = await axios.post(
          `${BASE_URL}/auth/refresh`,
          {},
          {
            headers: {
              Authorization: `Bearer ${getLocalRefreshToken()}`,
            },
          },
        )

        const { accessToken, refreshToken } = response.data

        setUser(accessToken, refreshToken)
        originalConfig.headers.Authorization = `Bearer ${accessToken}`
        api.defaults.headers.common['Authorization'] = 'Bearer ' + accessToken

        return api(originalConfig)
      } catch (_error) {
        removeUser()

        await router.push('auth')

        return Promise.reject(_error)
      }
    }

    return Promise.reject(err)
  },
)
export default api
