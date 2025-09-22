import { defineStore } from 'pinia'
import { bookingAPI } from '@/api/booking'
import { useToast } from 'vue-toastification'

const toast = useToast()

export const useBookingStore = defineStore('booking', {
    state: () => ({
        // Session
        sessionId: null,

        // Shows
        shows: [],
        currentShow: null,

        // Performance
        performances: [],
        selectedPerformance: null,

        // Seats
        seatMap: null,
        selectedSeats: [],
        reservationExpiry: null,

        // Customer
        customerInfo: {
            customer_name: '',
            customer_email: '',
            customer_phone: '',
            customer_id_number: '',
            notes: ''
        },

        // Booking
        currentBooking: null,
        bookingCode: null,

        // Payment
        currentTransaction: null,

        // UI State
        loading: false,
    }),

    getters: {
        totalAmount: (state) => {
            return state.selectedSeats.reduce((sum, seat) => sum + seat.price, 0)
        },

        serviceFee: (state) => {
            return state.selectedSeats.length * 10000
        },

        finalAmount: (state) => {
            return state.totalAmount + state.serviceFee
        }
    },

    actions: {
        // Initialize session
        initSession() {
            if (!this.sessionId) {
                this.sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
                sessionStorage.setItem('session_id', this.sessionId)
            }
        },

        // Load all shows
        async loadShows() {
            try {
                this.loading = true
                const response = await bookingAPI.getShows()
                this.shows = response.data.results || response.data
            } catch (error) {
                console.error('Failed to load shows:', error)
                throw error
            } finally {
                this.loading = false
            }
        },

        // Load show detail
        async loadShowDetail(showId) {
            try {
                this.loading = true
                const response = await bookingAPI.getShowDetail(showId)
                this.currentShow = response.data
                this.performances = response.data.performances || []
            } catch (error) {
                console.error('Failed to load show detail:', error)
                throw error
            } finally {
                this.loading = false
            }
        },

        // Load seat map
        async loadSeatMap(performanceId) {
            try {
                this.loading = true
                const response = await bookingAPI.getSeatMap(performanceId)
                this.seatMap = response.data
            } catch (error) {
                console.error('Failed to load seat map:', error)
                throw error
            } finally {
                this.loading = false
            }
        },

        // Toggle seat selection
        async toggleSeat(seat) {
            const index = this.selectedSeats.findIndex(s => s.id === seat.id)

            if (index > -1) {
                // Deselect
                const seatToRemove = this.selectedSeats[index]
                this.selectedSeats.splice(index, 1)

                // Release seat
                try {
                    await bookingAPI.releaseSeats([seatToRemove.id], this.sessionId)
                } catch (error) {
                    console.error('Failed to release seat:', error)
                }
            } else {
                // Select
                if (this.selectedSeats.length >= 8) {
                    toast.warning('Bạn chỉ có thể chọn tối đa 8 ghế')
                    return
                }

                // Reserve seats
                try {
                    const response = await bookingAPI.reserveSeats(
                        this.selectedPerformance.id,
                        [...this.selectedSeats.map(s => s.id), seat.id],
                        this.sessionId
                    )

                    this.selectedSeats = response.data.seats
                    this.reservationExpiry = response.data.expires_at

                    toast.success('Đã giữ ghế thành công!')
                } catch (error) {
                    toast.error('Không thể giữ ghế này')
                }
            }
        },

        // Create booking
        async createBooking() {
            try {
                this.loading = true

                const bookingData = {
                    performance_id: this.selectedPerformance.id,
                    seat_ids: this.selectedSeats.map(s => s.id),
                    session_id: this.sessionId,
                    ...this.customerInfo
                }

                const response = await bookingAPI.createBooking(bookingData)
                this.currentBooking = response.data
                this.bookingCode = response.data.booking_code

                toast.success('Đặt vé thành công!')
                return response.data
            } catch (error) {
                console.error('Failed to create booking:', error)
                throw error
            } finally {
                this.loading = false
            }
        },

        // Process payment
        async processPayment(paymentMethod) {
            try {
                this.loading = true
                const response = await bookingAPI.createPayment(this.bookingCode, paymentMethod)

                this.currentTransaction = response.data.transaction_id

                // If payment_url exists, it means we need to redirect (VNPay, MoMo, etc.)
                if (response.data.payment_url) {
                    return response.data // Return data to let component handle redirect
                }

                // Fallback for mock/auto payment
                if (response.data.auto_complete) {
                    this.startPaymentStatusPolling(response.data.transaction_id)
                }

                return response.data
            } catch (error) {
                console.error('Payment failed:', error)
                throw error
            } finally {
                this.loading = false
            }
        },

        // Poll payment status
        async startPaymentStatusPolling(transactionId) {
            const checkStatus = async () => {
                try {
                    const response = await bookingAPI.checkPaymentStatus(transactionId)

                    if (response.data.status === 'success') {
                        toast.success('Thanh toán thành công!')
                        this.clearSession()
                        return true
                    } else if (response.data.status === 'failed') {
                        toast.error('Thanh toán thất bại!')
                        return false
                    }

                    // Continue polling if pending
                    if (response.data.status === 'pending') {
                        setTimeout(checkStatus, 5000) // Check every 5 seconds
                    }
                } catch (error) {
                    console.error('Failed to check payment status:', error)
                }
            }

            // Start checking after 5 seconds
            setTimeout(checkStatus, 5000)
        },

        // Clear session
        clearSession() {
            this.selectedSeats = []
            this.customerInfo = {
                customer_name: '',
                customer_email: '',
                customer_phone: '',
                customer_id_number: '',
                notes: ''
            }
            this.reservationExpiry = null
            this.selectedPerformance = null
            sessionStorage.removeItem('session_id')
            this.sessionId = null
        }
    }
})