import { createRouter, createWebHistory } from 'vue-router'
import { sessionManager } from '@/utils/sessionManager'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../pages/HomePage.vue')
    },
    {
        path: '/lookup',
        name: 'Lookup',
        component: () => import('../pages/LookupPage.vue')
    },
    {
        path: '/booking/:showId',
        name: 'SelectPerformance',
        component: () => import('../pages/SelectPerformance.vue')
    },
    {
        path: '/booking/:showId/seats',
        name: 'SelectSeats',
        component: () => import('../pages/SelectSeats.vue'),
        meta: {
            requiresSession: true,
            requiredKeys: ['session_id', 'selectedPerformance']
        }
    },
    {
        path: '/booking/:showId/customer-info',
        name: 'CustomerInfo',
        component: () => import('../pages/CustomerInfo.vue'),
        meta: {
            requiresSession: true,
            requiredKeys: ['session_id', 'selectedPerformance', 'selectedSeats', 'reservationExpiry']
        }
    },
    {
        path: '/booking/confirmation/:bookingCode',
        name: 'Confirmation',
        component: () => import('../pages/Confirmation.vue')
    },
    {
        path: '/payment/failed',
        name: 'PaymentFailed',
        component: () => import('../pages/PaymentFailed.vue')
    },
    {
        path: '/payment/error',
        name: 'PaymentError',
        component: () => import('../pages/PaymentError.vue')
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        }
        if (to.hash) {
            return {
                el: to.hash,
                behavior: 'smooth',
            }
        }
        return { top: 0, behavior: 'smooth' }
    }
})

router.beforeEach(async (to, from, next) => {
    if (to.meta.requiresSession) {
        const sessionId = sessionManager.get('session_id')

        if (!sessionId) {
            console.warn('❌ No session ID found, redirecting to home')
            sessionManager.clearBookingSession()
            return next({ name: 'Home' })
        }

        const requiredKeys = to.meta.requiredKeys || []
        if (!sessionManager.validateSession(requiredKeys)) {
            console.warn('❌ Invalid session data, redirecting to home')
            sessionManager.clearBookingSession()

            const selectedSeats = sessionManager.get('selectedSeats')
            if (selectedSeats?.length > 0) {
                try {
                    await bookingAPI.releaseSeats(
                        selectedSeats.map(s => s.id),
                        sessionId
                    )
                } catch (error) {
                    console.error('Failed to release seats:', error)
                }
            }

            return next({ name: 'Home' })
        }
    }
    if (to.name === 'CustomerInfo') {
        const hasSeats = sessionStorage.getItem('selectedSeats')
        if (!hasSeats) {
            next({ name: 'SelectPerformance', params: { showId: to.params.showId } })
            return
        }
    }

    next()
})

export default router
