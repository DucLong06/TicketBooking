
import axios from 'axios'
import { useToast } from 'vue-toastification'

const toast = useToast()

// Create axios instance
const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api',  
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    }
})

// Request interceptor
api.interceptors.request.use(
    config => {
        // Add session ID for seat reservation
        const sessionId = sessionStorage.getItem('session_id')
        if (sessionId) {
            // Add session_id to data for POST requests
            if (config.method === 'post' && config.data) {
                config.data.session_id = sessionId
            }
        }

        return config
    },
    error => {
        return Promise.reject(error)
    }
)

// Response interceptor
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response) {
            const message = error.response.data?.error || error.response.data?.message || 'Có lỗi xảy ra'
            toast.error(message)
        } else {
            toast.error('Không thể kết nối đến server')
        }
        return Promise.reject(error)
    }
)

export default api