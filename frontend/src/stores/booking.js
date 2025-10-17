import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { bookingAPI } from '@/api/booking'
import { useToast } from 'vue-toastification'

export const useBookingStore = defineStore('booking', () => {
    const toast = useToast()

    // Helper function to format price
    const formatPrice = (price) => {
        if (price === undefined || price === null) return '0 ₫';
        return new Intl.NumberFormat("vi-VN", {
            style: "currency",
            currency: "VND",
        }).format(price);
    };

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
        shipping_time: 'business_hours',
        notes: '',
        discount_code: ''
    })
    const currentBooking = ref(null)
    const bookingCode = ref(null)
    const currentTransaction = ref(null)
    const loading = ref(false)

    // Discount related state
    const discountMessage = ref('');
    const isDiscountSuccess = ref(false);

    // GETTERS
    const totalAmount = computed(() => {
        return selectedSeats.value.reduce((sum, seat) => sum + (seat.price || 0), 0)
    })

    const serviceFee = computed(() => {
        if (!currentShow.value?.service_fee_per_ticket) return 0;
        return selectedSeats.value.length * currentShow.value.service_fee_per_ticket;
    });

    const finalAmount = computed(() => {
        // Nếu đã có booking từ API (đã tính sẵn)
        if (currentBooking.value?.final_amount !== undefined) {
            return currentBooking.value.final_amount;
        }

        // Tính toán: ticket + service - discount
        const base = totalAmount.value + serviceFee.value;
        const discount = discountAmount.value || 0;
        return Math.max(0, base - discount);
    });

    const discountAmount = computed(() => {
        return currentBooking.value?.discount_amount || 0;
    });

    const showInfo = computed(() => {
        return currentShow.value || {}
    })

    // ACTIONS
    const initSession = () => {
        let sid = sessionStorage.getItem('session_id');
        if (!sid) {
            sid = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
            sessionStorage.setItem('session_id', sid)
        }
        sessionId.value = sid;
    }

    /**
     * Apply discount code WITHOUT creating a temporary booking
     * TODO: Update this to use validate API when backend is ready
     */
    const applyDiscount = async (code, currentCustomerInfo = {}) => {
        if (!selectedPerformance.value || selectedSeats.value.length === 0) {
            toast.error("Vui lòng chọn ghế trước khi áp dụng mã.");
            return;
        }

        if (!code || !code.trim()) {
            toast.warning("Vui lòng nhập mã giảm giá.");
            return;
        }

        try {
            // Reset previous state
            isDiscountSuccess.value = false;
            discountMessage.value = '';

            // TEMPORARY: Still using createBooking with temp data
            // TODO: Replace with validateDiscountCode API
            const bookingData = {
                performance_id: selectedPerformance.value.id,
                seat_ids: selectedSeats.value.map(s => s.id),
                session_id: sessionId.value,
                customer_name: currentCustomerInfo.fullName || 'temp',
                customer_email: currentCustomerInfo.email || 'temp@example.com',
                customer_phone: currentCustomerInfo.phone || '0000000000',
                customer_address: currentCustomerInfo.address || 'temp',
                shipping_time: currentCustomerInfo.shippingTime || 'business_hours',
                notes: currentCustomerInfo.notes || '',
                discount_code: code.trim(),
            };

            const response = await bookingAPI.createBooking(bookingData);

            // Store the booking with discount info
            currentBooking.value = response.data;
            bookingCode.value = response.data.booking_code;

            // Update customer info to include discount code
            customerInfo.value.discount_code = code.trim();

            isDiscountSuccess.value = true;
            discountMessage.value = `Áp dụng thành công! Bạn được giảm ${formatPrice(response.data.discount_amount)}.`;

            toast.success(discountMessage.value);

        } catch (error) {
            const errorMessage = error.response?.data?.discount_code?.[0] ||
                "Mã giảm giá không hợp lệ hoặc có lỗi xảy ra.";

            isDiscountSuccess.value = false;
            discountMessage.value = errorMessage;
            customerInfo.value.discount_code = '';

            // Reset discount if was applied before
            if (currentBooking.value) {
                currentBooking.value.discount_amount = 0;
                currentBooking.value.discount = null;
                const serviceFeeCalc = currentBooking.value.service_fee || serviceFee.value;
                currentBooking.value.final_amount =
                    currentBooking.value.total_amount + serviceFeeCalc;
            }

            toast.error(errorMessage);
        }
    }

    const createBooking = async () => {
        try {
            loading.value = true

            if (!selectedPerformance.value?.id) throw new Error('NO_PERFORMANCE')
            if (!selectedSeats.value?.length) throw new Error('NO_SEATS')
            if (!sessionId.value) throw new Error('NO_SESSION_ID')

            const bookingData = {
                performance_id: selectedPerformance.value.id,
                seat_ids: selectedSeats.value.map(s => s.id),
                session_id: sessionId.value,
                ...customerInfo.value
            }

            const response = await bookingAPI.createBooking(bookingData)

            if (!response.data.seat_reservations?.length) {
                throw new Error('NO_SEATS_IN_BOOKING')
            }

            currentBooking.value = response.data
            bookingCode.value = response.data.booking_code

            if (response.data.expires_at) {
                const expiresAt = new Date(response.data.expires_at);
                sessionStorage.setItem('bookingExpiry', expiresAt.toISOString());
            }
            sessionStorage.setItem('currentBooking', JSON.stringify(response.data))

            return response.data
        } catch (error) {
            clearBooking()
            let errorMessage = 'Có lỗi xảy ra khi tạo đơn hàng.'
            if (error.response?.data?.error) {
                errorMessage = error.response.data.error
            } else if (error.response?.data?.detail) {
                errorMessage = error.response.data.detail
            }
            const enhancedError = new Error(errorMessage)
            enhancedError.shouldRedirect = true
            throw enhancedError
        } finally {
            loading.value = false
        }
    }

    const processPayment = async (paymentMethod) => {
        try {
            loading.value = true
            const response = await bookingAPI.createPayment(bookingCode.value, paymentMethod)
            currentTransaction.value = response.data.transaction_id

            // Clear session data related to seat selection to prevent accidental release
            // after the user is sent to the payment gateway.
            selectedSeats.value = []
            reservationExpiry.value = null
            sessionStorage.removeItem('selectedSeats')
            sessionStorage.removeItem('reservationExpiry')

            return response.data
        } catch (error) {
            console.error('Failed to process payment:', error)
            throw error
        } finally {
            loading.value = false
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

            // Store show in session
            sessionStorage.setItem('currentShow', JSON.stringify(response.data))
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

    const resetDiscount = () => {
        isDiscountSuccess.value = false
        discountMessage.value = ''
        customerInfo.value.discount_code = ''

        if (currentBooking.value) {
            currentBooking.value.discount_amount = 0
            currentBooking.value.discount = null

            // Recalculate final amount without discount
            const serviceFeeCalc = currentBooking.value.service_fee || serviceFee.value;
            currentBooking.value.final_amount =
                currentBooking.value.total_amount + serviceFeeCalc;
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
            shipping_time: 'business_hours',
            notes: '',
            discount_code: ''
        }
        isDiscountSuccess.value = false;
        discountMessage.value = '';

        sessionStorage.removeItem('selectedSeats')
        sessionStorage.removeItem('bookingData')
        sessionStorage.removeItem('bookingExpiry')
        sessionStorage.removeItem('reservationExpiry')
        sessionStorage.removeItem('currentBooking')
    }

    return {
        // State
        sessionId, shows, currentShow, performances, selectedPerformance, seatMap,
        selectedSeats, reservationExpiry, customerInfo, currentBooking, bookingCode,
        currentTransaction, loading,

        // Computed
        totalAmount, serviceFee, finalAmount, showInfo,
        discountAmount, discountMessage, isDiscountSuccess,

        // Actions
        initSession, applyDiscount, loadShows, loadShowDetail,
        setSelectedPerformance, createBooking, processPayment,
        clearBooking, resetDiscount,
    }
})