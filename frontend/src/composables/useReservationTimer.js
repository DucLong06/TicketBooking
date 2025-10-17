import { ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

export function useReservationTimer(expiryKey = 'reservationExpiry') {
    const timeLeft = ref(0)
    const router = useRouter()
    const toast = useToast()
    let timer = null

    const startTimer = (expiryISO, redirectPath = '/') => {
        if (!expiryISO) {
            console.error('No expiry time provided')
            return
        }

        const expiryDate = new Date(expiryISO)

        // Clear existing timer
        stopTimer()

        timer = setInterval(() => {
            const now = new Date()
            const diff = Math.floor((expiryDate - now) / 1000)
            timeLeft.value = Math.max(0, diff)

            if (timeLeft.value === 0) {
                stopTimer()
                toast.error('Hết thời gian giữ ghế')
                router.push(redirectPath)
            }
        }, 1000)
    }

    const stopTimer = () => {
        if (timer) {
            clearInterval(timer)
            timer = null
        }
    }

    onUnmounted(() => {
        stopTimer()
    })

    return {
        timeLeft,
        startTimer,
        stopTimer
    }
}