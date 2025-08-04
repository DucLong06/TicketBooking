import api from './index'

export const bookingAPI = {
    // Get all shows
    getShows() {
        return api.get('/shows/')
    },

    // Get show detail
    getShowDetail(showId) {
        return api.get(`/shows/${showId}/`)
    },

    // Get performances for a show
    getPerformances(showId) {
        return api.get(`/shows/${showId}/performances/`)
    },

    // Get seat map for performance
    getSeatMap(performanceId) {
        return api.get(`/performances/${performanceId}/seat-map/`)
    },

    // Reserve seats
    reserveSeats(performanceId, seatIds, sessionId) {
        return api.post('/seats/reserve/', {
            performance_id: performanceId,
            seat_ids: seatIds,
            session_id: sessionId
        })
    },

    // Release seats
    releaseSeats(seatIds, sessionId) {
        return api.post('/seats/release/', {
            seat_ids: seatIds,
            session_id: sessionId
        })
    },

    // Create booking
    createBooking(data) {
        return api.post('/bookings/', data)
    },

    // Get booking detail
    getBooking(bookingCode) {
        return api.get(`/bookings/${bookingCode}/`)
    },

    // Create payment
    createPayment(bookingCode, paymentMethod) {
        return api.post(`/bookings/${bookingCode}/payment/`, {
            payment_method: paymentMethod
        })
    },

    // Check payment status
    checkPaymentStatus(transactionId) {
        return api.get(`/payment/${transactionId}/status/`)
    }
}