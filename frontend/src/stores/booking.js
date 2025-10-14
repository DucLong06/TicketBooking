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

    // Discount related state - Simplified
    const discountMessage = ref('');
    const isDiscountSuccess = ref(false);

    // GETTERS
    const totalAmount = computed(() => {
        return selectedSeats.value.reduce((sum, seat) => sum + (seat.price || 0), 0)
    })

    const finalAmount = computed(() => {
        if (currentBooking.value) {
            return currentBooking.value.final_amount;
        }
        const serviceFee = (currentShow.value?.service_fee_per_ticket || 10000) * selectedSeats.value.length;
        return totalAmount.value + serviceFee;
    });

    const discountAmount = computed(() => currentBooking.value?.discount_amount || 0);

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

    // This function now acts as a "preview" by creating/updating a pending booking
    const applyDiscount = async (code, currentCustomerInfo) => {
        if (!selectedPerformance.value || selectedSeats.value.length === 0) {
            toast.error("Vui lòng chọn ghế trước khi áp dụng mã.");
            return;
        }

        try {
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
                discount_code: code,
            };

            const response = await bookingAPI.createBooking(bookingData);
            currentBooking.value = response.data;
            bookingCode.value = response.data.booking_code; // Important for subsequent payment

            isDiscountSuccess.value = true;
            discountMessage.value = `Áp dụng thành công! Bạn được giảm ${formatPrice(response.data.discount_amount)}.`;
            toast.success(discountMessage.value);

        } catch (error) {
            const errorMessage = error.response?.data?.discount_code?.[0] || "Mã giảm giá không hợp lệ hoặc có lỗi xảy ra.";
            isDiscountSuccess.value = false;
            discountMessage.value = errorMessage;

            // Reset discount values in any existing booking preview
            if (currentBooking.value) {
                currentBooking.value.discount_amount = 0;
                currentBooking.value.discount = null;
                currentBooking.value.final_amount = currentBooking.value.total_amount + currentBooking.value.service_fee;
            }

            toast.error(errorMessage);
        }
    }


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

            if (response.data.expires_at) {
                const expiresAt = new Date(response.data.expires_at);
                sessionStorage.setItem('bookingExpiry', expiresAt.toISOString());
            }

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

    // Other actions like loadShows, loadShowDetail etc. remain unchanged...
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
    }

    return {
        sessionId, shows, currentShow, performances, selectedPerformance, seatMap,
        selectedSeats, reservationExpiry, customerInfo, currentBooking, bookingCode,
        currentTransaction, loading, totalAmount, finalAmount, showInfo,
        discountAmount, discountMessage, isDiscountSuccess,
        initSession, applyDiscount, loadShows, loadShowDetail,
        setSelectedPerformance, createBooking, processPayment, clearBooking
    }
})