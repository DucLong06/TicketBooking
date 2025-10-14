import { onBeforeUnmount, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { bookingAPI } from '@/api/booking'
import { sessionManager } from '@/utils/sessionManager'

export function useBookingCleanup(options = {}) {
    const router = useRouter()
    const {
        shouldRelease = true,
        excludeRoutes = [
            '/booking/confirmation',
            '/payment/failed',
            '/payment/error'
        ]
    } = options

    const releaseSeats = async () => {
        if (!shouldRelease) return

        const sessionId = sessionManager.get('session_id')
        const selectedSeats = sessionManager.get('selectedSeats')

        if (sessionId && selectedSeats?.length > 0) {
            try {
                await bookingAPI.releaseSeats(
                    selectedSeats.map(s => s.id),
                    sessionId
                )
            } catch (error) {
                console.error('❌ Failed to release seats:', error)
            }
        }
    }

    const cleanup = async () => {
        await releaseSeats()
        sessionManager.clearBookingSession()
    }

    // Xử lý beforeunload (F5, đóng tab)
    const handleBeforeUnload = (e) => {
        const currentPath = window.location.pathname

        // Không clear nếu đang ở trang completion
        if (excludeRoutes.some(route => currentPath.includes(route))) {
            return
        }

        // Sử dụng sendBeacon để gửi request async khi đóng trang
        const sessionId = sessionManager.get('session_id')
        const selectedSeats = sessionManager.get('selectedSeats')

        if (sessionId && selectedSeats?.length > 0) {
            const data = JSON.stringify({
                session_id: sessionId,
                seat_ids: selectedSeats.map(s => s.id)
            })

            navigator.sendBeacon('/api/seats/release/', data)
        }

        // Clear session
        sessionManager.clearBookingSession()
    }

    onMounted(() => {
        window.addEventListener('beforeunload', handleBeforeUnload)
    })

    onBeforeUnmount(() => {
        window.removeEventListener('beforeunload', handleBeforeUnload)
    })

    return {
        cleanup,
        releaseSeats
    }
}