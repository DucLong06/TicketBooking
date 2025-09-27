import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../pages/HomePage.vue')
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
    },
    {
        path: '/booking/:showId/customer-info',
        name: 'CustomerInfo',
        component: () => import('../pages/CustomerInfo.vue'),
    },
    {
        path: '/booking/:showId/payment',
        name: 'Payment',
        component: () => import('../pages/Payment.vue'),
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
    routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
    // Check session for booking flow
    if (to.meta.requiresSession) {
        const sessionId = sessionStorage.getItem('session_id')
        if (!sessionId) {
            next({ name: 'Home' })
            return
        }
    }
    next()
})

export default router