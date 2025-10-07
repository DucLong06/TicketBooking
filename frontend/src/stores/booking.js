import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { bookingAPI } from '@/api/booking'
import { useToast } from 'vue-toastification'

export const useBookingStore = defineStore('booking', () => {
    const toast = useToast()

    // STATE
    // Session
    const sessionId = ref(null)

    // Shows
    const shows = ref([])
    const currentShow = ref(null)

    // Performance
    const performances = ref([])
    const selectedPerformance = ref(null)

    // Seats
    const seatMap = ref(null)
    const selectedSeats = ref([])
    const reservationExpiry = ref(null)

    // Customer
    const customerInfo = ref({
        customer_name: '',
        customer_email: '',
        customer_phone: '',
        customer_id_number: '',
        notes: ''
    })

    // Booking
    const currentBooking = ref(null)
    const bookingCode = ref(null)

    // Payment
    const currentTransaction = ref(null)

    // UI State
    const loading = ref(false)

    // GETTERS (computed)
    const totalAmount = computed(() => {
        return selectedSeats.value.reduce((sum, seat) => sum + seat.price, 0)
    })

    const serviceFee = computed(() => {
        return selectedSeats.value.length * 10000
    })

    const finalAmount = computed(() => {
        return totalAmount.value + serviceFee.value
    })

    // ACTIONS (functions)

    // Initialize session
    const initSession = () => {
        if (!sessionId.value) {
            sessionId.value = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
            sessionStorage.setItem('session_id', sessionId.value)
        }
    }

    // Load all shows
    const loadShows = async () => {
        try {
            loading.value = true
            const response = await bookingAPI.getShows()
            shows.value = response.data.results || response.data

        } catch (error) {
            console.error('Failed to load shows:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    // Load show detail
    const loadShowDetail = async (showId) => {
        try {
            loading.value = true
            const response = await bookingAPI.getShowDetail(showId)
            currentShow.value = response.data
            performances.value = response.data.performances || []
        } catch (error) {
            console.error('Failed to load show detail:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    // Set selected performance
    const setSelectedPerformance = (performance) => {
        selectedPerformance.value = performance
        sessionStorage.setItem('selectedPerformance', JSON.stringify(performance))
    }

    // Load seat map
    const loadSeatMap = async (performanceId) => {
        try {
            loading.value = true
            const response = await bookingAPI.getSeatMap(performanceId)
            seatMap.value = response.data
        } catch (error) {
            console.error('Failed to load seat map:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    // Toggle seat selection
    const toggleSeat = async (seat) => {
        const index = selectedSeats.value.findIndex(s => s.id === seat.id)

        if (index > -1) {
            // Deselect
            const seatToRemove = selectedSeats.value[index]
            selectedSeats.value.splice(index, 1)

            // Release seat
            try {
                await bookingAPI.releaseSeats([seatToRemove.id], sessionId.value)
            } catch (error) {
                console.error('Failed to release seat:', error)
            }
        } else {
            // Select
            if (selectedSeats.value.length >= 8) {
                toast.warning('Bạn chỉ có thể chọn tối đa 8 ghế')
                return
            }

            // Reserve seats
            try {
                const response = await bookingAPI.reserveSeats(
                    selectedPerformance.value.id,
                    [...selectedSeats.value.map(s => s.id), seat.id],
                    sessionId.value
                )

                selectedSeats.value = response.data.seats
                reservationExpiry.value = response.data.expires_at

                toast.success('Đã giữ ghế thành công!')
            } catch (error) {
                toast.error('Không thể giữ ghế này')
            }
        }
    }

    // Create booking
    const createBooking = async () => {
        try {
            loading.value = true

            const bookingData = {
                performance_id: selectedPerformance.value.id,
                seat_ids: selectedSeats.value.map(s => s.id),
                session_id: sessionId.value,
                ...customerInfo.value
            }

            const response = await bookingAPI.createBooking(bookingData)
            currentBooking.value = response.data
            bookingCode.value = response.data.booking_code

            // Save comprehensive booking data to sessionStorage
            const completeBookingData = {
                showInfo: {
                    name: selectedPerformance.value.show_name || currentShow.value?.name
                },
                performance: {
                    date: new Date(selectedPerformance.value.datetime).toLocaleDateString("vi-VN"),
                    time: new Date(selectedPerformance.value.datetime).toLocaleTimeString("vi-VN", {
                        hour: "2-digit",
                        minute: "2-digit",
                    })
                },
                customerInfo: {
                    fullName: customerInfo.value.customer_name,
                    email: customerInfo.value.customer_email,
                    phone: customerInfo.value.customer_phone
                },
                amount: finalAmount.value,
                selectedSeats: selectedSeats.value,
                bookingCode: response.data.booking_code,
                status: response.data.status,
                // Keep raw response for debugging
                _rawResponse: response.data
            };

            sessionStorage.setItem('bookingData', JSON.stringify(completeBookingData));

            toast.success('Đặt vé thành công!')
            return response.data
        } catch (error) {
            console.error('Failed to create booking:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    // Process payment
    const processPayment = async (paymentMethod) => {
        try {
            loading.value = true
            const response = await bookingAPI.createPayment(bookingCode.value, paymentMethod)

            currentTransaction.value = response.data.transaction_id

            // If payment_url exists, it means we need to redirect (VNPay, MoMo, etc.)
            if (response.data.payment_url) {
                return response.data // Return data to let component handle redirect
            }

            // Fallback for mock/auto payment
            if (response.data.auto_complete) {
                startPaymentStatusPolling(response.data.transaction_id)
            }

            return response.data
        } catch (error) {
            console.error('Payment failed:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    // Check payment status
    const checkPaymentStatus = async (transactionId) => {
        try {
            const response = await bookingAPI.checkPaymentStatus(transactionId)
            return response
        } catch (error) {
            console.error('Failed to check payment status:', error)
            throw error
        }
    }

    // Poll payment status
    const startPaymentStatusPolling = async (transactionId) => {
        const checkStatus = async () => {
            try {
                const response = await bookingAPI.checkPaymentStatus(transactionId)

                if (response.data.status === 'success') {
                    toast.success('Thanh toán thành công!')
                    clearSession()
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
    }

    // Clear session
    const clearSession = () => {
        selectedSeats.value = []
        customerInfo.value = {
            customer_name: '',
            customer_email: '',
            customer_phone: '',
            customer_id_number: '',
            notes: ''
        }
        reservationExpiry.value = null
        selectedPerformance.value = null
        sessionStorage.removeItem('session_id')
        sessionId.value = null
    }

    // Return all state and methods
    return {
        // State
        sessionId,
        shows,
        currentShow,
        performances,
        selectedPerformance,
        seatMap,
        selectedSeats,
        reservationExpiry,
        customerInfo,
        currentBooking,
        bookingCode,
        currentTransaction,
        loading,

        // Getters
        totalAmount,
        serviceFee,
        finalAmount,

        // Actions
        initSession,
        loadShows,
        loadShowDetail,
        setSelectedPerformance,
        loadSeatMap,
        toggleSeat,
        createBooking,
        processPayment,
        checkPaymentStatus,
        startPaymentStatusPolling,
        clearSession
    }
})