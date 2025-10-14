import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { bookingAPI } from '@/api/booking'
import { useToast } from 'vue-toastification'

export const useBookingStore = defineStore('booking', () => {
    const toast = useToast()

    // STATE
    const sessionId = ref(null)
    const shows = ref([])
    const currentShow = ref(null)
    const performances = ref([])
    const selectedPerformance = ref(null)
    const seatMap = ref(null)
    const selectedSeats = ref([])
    const reservationExpiry = ref(null)
    const customerInfo = ref({
        customer_name: '',
        customer_email: '',
        customer_phone: '',
        customer_address: '',
        shipping_time: '',
        notes: ''
    })
    const currentBooking = ref(null)
    const bookingCode = ref(null)
    const currentTransaction = ref(null)
    const loading = ref(false)

    // Discount related state
    const discountCode = ref('');
    const discountAmount = ref(0);
    const discountMessage = ref('');
    const isDiscountSuccess = ref(false);


    // GETTERS
    const totalAmount = computed(() => {
        return selectedSeats.value.reduce((sum, seat) => sum + (seat.price || 0), 0)
    })

    const finalAmount = computed(() => {
        const baseAmount = totalAmount.value + (currentShow.value?.service_fee_per_ticket || 10000) * selectedSeats.value.length;
        return baseAmount - discountAmount.value;
    });

    const showInfo = computed(() => {
        return currentShow.value || {}
    })

    // ACTIONS
    const initSession = () => {
        if (!sessionId.value) {
            sessionId.value = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
            sessionStorage.setItem('session_id', sessionId.value)
        }
    }

    const applyDiscount = async (code) => {
        if (!bookingCode.value) {
            toast.error("Vui lòng tạo đơn hàng trước khi áp dụng mã.");
            return;
        }
        try {
            const response = await bookingAPI.applyDiscountCode(bookingCode.value, code);
            discountAmount.value = response.data.discount_amount;
            isDiscountSuccess.value = true;
            discountMessage.value = `Áp dụng thành công! Bạn được giảm ${formatPrice(discountAmount.value)}.`;
            toast.success("Áp dụng mã giảm giá thành công!");
        } catch (error) {
            discountAmount.value = 0;
            isDiscountSuccess.value = false;
            discountMessage.value = error.response?.data?.error || "Mã giảm giá không hợp lệ.";
            toast.error(discountMessage.value);
        }
    }

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

    const setSelectedPerformance = (performance) => {
        selectedPerformance.value = performance
        sessionStorage.setItem('selectedPerformance', JSON.stringify(performance))
    }

    const loadSeatMap = async (performanceId) => {
        try {
            loading.value = true
            const response = await bookingAPI.getSeatMap(performanceId)
            seatMap.value = response.data

            // Map existing reservations to selected seats format
            const existingReservations = response.data.seats
                .filter(seat => seat.status === 'selected')
                .map(seat => ({
                    id: seat.id,
                    row: seat.row,
                    number: seat.number,
                    display_number: seat.display_number,
                    full_label: seat.full_label,
                    section_id: seat.section_id,
                    section_name: seat.section_name,
                    price: seat.price,
                    price_category_color: seat.price_category_color,
                    effective_price_category_name: seat.effective_price_category_name
                }))

            if (existingReservations.length > 0) {
                selectedSeats.value = existingReservations
            }

            return response.data
        } catch (error) {
            console.error('Failed to load seat map:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    const selectSeat = async (seat) => {
        initSession()

        const isSelected = selectedSeats.value.some(s => s.id === seat.id)

        if (isSelected) {
            // Deselect
            try {
                await bookingAPI.releaseSeats({
                    session_id: sessionId.value,
                    seat_ids: [seat.id]
                })
                selectedSeats.value = selectedSeats.value.filter(s => s.id !== seat.id)
                toast.success('Đã bỏ chọn ghế')
            } catch (error) {
                toast.error('Không thể bỏ chọn ghế')
            }
        } else {
            // Select
            try {
                const response = await bookingAPI.reserveSeats({
                    performance_id: selectedPerformance.value.id,
                    seat_ids: [seat.id],
                    session_id: sessionId.value
                })

                // ===== CRITICAL: Use full seat data from API response =====
                if (response.data.seats && response.data.seats.length > 0) {
                    const reservedSeat = response.data.seats[0]
                    console.log("response.data:", response.data);

                    // Ensure we have all necessary fields for display
                    const seatData = {
                        id: reservedSeat.id,
                        row: reservedSeat.row,
                        number: reservedSeat.number,
                        display_number: reservedSeat.number, // display_label from API
                        full_label: reservedSeat.full_label,
                        section_id: seat.section_id, // from original seat object
                        section_name: reservedSeat.section_name,
                        price: reservedSeat.price,
                        price_category_color: seat.price_category_color, // from original
                        effective_price_category_name: seat.effective_price_category_name // from original
                    }

                    selectedSeats.value.push(seatData)
                    reservationExpiry.value = response.data.expires_at
                    toast.success('Đã chọn ghế')
                }
            } catch (error) {
                toast.error('Không thể giữ ghế này')
            }
        }
    }

    const createBooking = async () => {
        try {
            loading.value = true

            const bookingData = {
                performance_id: selectedPerformance.value.id,
                seat_ids: selectedSeats.value.map(s => s.id),
                session_id: sessionId.value,
                discount_code: discountCode.value,
                ...customerInfo.value
            }

            const response = await bookingAPI.createBooking(bookingData)

            currentBooking.value = response.data
            bookingCode.value = response.data.booking_code

            if (response.data.expires_at) {
                const expiresAt = new Date(response.data.expires_at);
                sessionStorage.setItem('bookingExpiry', expiresAt.toISOString());
            }

            // ===== Save complete booking data with FULL seat info =====
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
                seats: selectedSeats.value,
                bookingCode: response.data.booking_code,
                status: response.data.status,
                _rawResponse: response.data
            }

            sessionStorage.setItem('bookingData', JSON.stringify(completeBookingData))

            return response.data
        } catch (error) {
            console.error('Failed to create booking:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    const processPayment = async (paymentMethod) => {
        try {
            loading.value = true
            const response = await bookingAPI.createPayment(bookingCode.value, paymentMethod)
            currentTransaction.value = response.data.transaction_id
            return response.data
        } catch (error) {
            console.error('Failed to process payment:', error)
            throw error
        } finally {
            loading.value = false
        }
    }

    const checkPaymentStatus = async (transactionId) => {
        try {
            const response = await bookingAPI.checkPaymentStatus(transactionId)
            return response
        } catch (error) {
            console.error('Failed to check payment status:', error)
            throw error
        }
    }

    const clearBooking = () => {
        selectedSeats.value = []
        currentBooking.value = null
        bookingCode.value = null
        customerInfo.value = {
            customer_name: '',
            customer_email: '',
            customer_phone: '',
            customer_address: '',
            shipping_time: '',
            notes: ''
        }
        sessionStorage.removeItem('selectedSeats')
        sessionStorage.removeItem('bookingData')
    }

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
        finalAmount,
        showInfo,

        // Discount related state
        discountCode,
        discountAmount,
        discountMessage,
        isDiscountSuccess,

        // Actions
        initSession,
        applyDiscount,
        loadShows,
        loadShowDetail,
        setSelectedPerformance,
        loadSeatMap,
        selectSeat,
        createBooking,
        processPayment,
        checkPaymentStatus,
        clearBooking
    }
})