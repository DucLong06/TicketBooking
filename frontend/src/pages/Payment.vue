<template>
	<DefaultLayout>
		<div class="container mx-auto px-4 py-8">
			<!-- Breadcrumb -->
			<nav class="mb-6">
				<ol class="flex items-center space-x-2 text-sm">
					<li>
						<router-link
							to="/"
							class="text-gray-500 hover:text-primary-600"
						>
							Trang chủ
						</router-link>
					</li>
					<li class="text-gray-400">/</li>
					<li>Chọn suất diễn</li>
					<li class="text-gray-400">/</li>
					<li>Chọn ghế</li>
					<li class="text-gray-400">/</li>
					<li>Thông tin khách hàng</li>
					<li class="text-gray-400">/</li>
					<li class="text-gray-700 font-medium">Thanh toán</li>
				</ol>
			</nav>

			<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
				<!-- Payment Methods - 2 columns -->
				<div class="lg:col-span-2">
					<div class="bg-white rounded-lg shadow-lg p-6">
						<h2 class="text-2xl font-bold mb-6">
							Phương thức thanh toán
						</h2>

						<!-- Payment Methods -->
						<div class="space-y-4">
							<!-- VNPay -->
							<div
								@click="selectPaymentMethod('vnpay')"
								:class="[
									'border-2 rounded-lg p-4 cursor-pointer transition',
									selectedMethod === 'vnpay'
										? 'border-primary-600 bg-primary-50'
										: 'border-gray-200 hover:border-gray-300',
								]"
							>
								<div class="flex items-center justify-between">
									<div class="flex items-center space-x-3">
										<input
											type="radio"
											:checked="
												selectedMethod === 'vnpay'
											"
											class="text-primary-600"
										/>
										<div>
											<div class="font-semibold">
												VNPay
											</div>
											<div class="text-sm text-gray-600">
												Thanh toán qua ví điện tử VNPay
											</div>
										</div>
									</div>
									<img
										src="https://vnpay.vn/assets/images/logo-icon/logo-primary.svg"
										alt="VNPay"
										class="h-8"
									/>
								</div>
							</div>
                            <!-- 9 pay -->
							<div
								@click="selectPaymentMethod('9pay')"
								:class="[
									'border-2 rounded-lg p-4 cursor-pointer transition',
									selectedMethod === '9pay'
										? 'border-primary-600 bg-primary-50'
										: 'border-gray-200 hover:border-gray-300',
								]"
							>
								<div class="flex items-center justify-between">
									<div class="flex items-center space-x-3">
										<input
											type="radio"
											:checked="selectedMethod === '9pay'"
											class="text-primary-600"
										/>
										<div>
											<div class="font-semibold">
												9Pay
											</div>
											<div class="text-sm text-gray-600">
												Thanh toán qua Cổng thanh toán
												9Pay
											</div>
										</div>
									</div>
									<img
										src="https://9pay.vn/assets/images/logo-icon/logo-primary.svg"
										alt="9Pay"
										class="h-8"
									/>
								</div>
							</div>
							<!-- Bank Transfer -->
							<!-- <div
								@click="selectPaymentMethod('bank')"
								:class="[
									'border-2 rounded-lg p-4 cursor-pointer transition',
									selectedMethod === 'bank'
										? 'border-primary-600 bg-primary-50'
										: 'border-gray-200 hover:border-gray-300',
								]"
							>
								<div class="flex items-center justify-between">
									<div class="flex items-center space-x-3">
										<input
											type="radio"
											:checked="selectedMethod === 'bank'"
											class="text-primary-600"
										/>
										<div>
											<div class="font-semibold">
												Chuyển khoản ngân hàng
											</div>
											<div class="text-sm text-gray-600">
												ATM/Internet Banking
											</div>
										</div>
									</div>
									<div class="flex space-x-2">
										<span
											class="text-xs bg-gray-100 px-2 py-1 rounded"
											>VCB</span
										>
										<span
											class="text-xs bg-gray-100 px-2 py-1 rounded"
											>TCB</span
										>
										<span
											class="text-xs bg-gray-100 px-2 py-1 rounded"
											>MB</span
										>
									</div>
								</div>
							</div> -->

							<!-- Momo -->
							<!-- <div
								@click="selectPaymentMethod('momo')"
								:class="[
									'border-2 rounded-lg p-4 cursor-pointer transition',
									selectedMethod === 'momo'
										? 'border-primary-600 bg-primary-50'
										: 'border-gray-200 hover:border-gray-300',
								]"
							>
								<div class="flex items-center justify-between">
									<div class="flex items-center space-x-3">
										<input
											type="radio"
											:checked="selectedMethod === 'momo'"
											class="text-primary-600"
										/>
										<div>
											<div class="font-semibold">
												Ví MoMo
											</div>
											<div class="text-sm text-gray-600">
												Thanh toán qua ví điện tử MoMo
											</div>
										</div>
									</div>
									<div
										class="w-8 h-8 bg-pink-500 rounded-full flex items-center justify-center"
									>
										<span
											class="text-white font-bold text-xs"
											>M</span
										>
									</div>
								</div>
							</div> -->

							<!-- Credit Card -->
							<!-- <div
								@click="selectPaymentMethod('card')"
								:class="[
									'border-2 rounded-lg p-4 cursor-pointer transition',
									selectedMethod === 'card'
										? 'border-primary-600 bg-primary-50'
										: 'border-gray-200 hover:border-gray-300',
								]"
							>
								<div class="flex items-center justify-between">
									<div class="flex items-center space-x-3">
										<input
											type="radio"
											:checked="selectedMethod === 'card'"
											class="text-primary-600"
										/>
										<div>
											<div class="font-semibold">
												Thẻ quốc tế
											</div>
											<div class="text-sm text-gray-600">
												Visa, Mastercard, JCB
											</div>
										</div>
									</div>
									<div class="flex space-x-2">
										<span
											class="text-xs bg-blue-100 px-2 py-1 rounded"
											>VISA</span
										>
										<span
											class="text-xs bg-red-100 px-2 py-1 rounded"
											>Master</span
										>
									</div>
								</div>
							</div> -->
						</div>

						<!-- Customer Info Summary -->
						<!-- <div class="mt-8 p-4 bg-gray-50 rounded-lg">
							<h3 class="font-semibold mb-3">
								Thông tin người đặt
							</h3>
							<div class="grid grid-cols-2 gap-4 text-sm">
								<div>
									<span class="text-gray-600">Họ tên:</span>
									<span class="ml-2 font-medium">{{
										customerInfo.fullName
									}}</span>
								</div>
								<div>
									<span class="text-gray-600">SĐT:</span>
									<span class="ml-2 font-medium">{{
										customerInfo.phone
									}}</span>
								</div>
								<div class="col-span-2">
									<span class="text-gray-600">Email:</span>
									<span class="ml-2 font-medium">{{
										customerInfo.email
									}}</span>
								</div>
							</div>
						</div> -->

						<!-- Action Buttons -->
						<div class="mt-8 flex justify-between">
							<button
								@click="goBack"
								class="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition"
							>
								← Quay lại
							</button>
							<button
								@click="processPayment"
								:disabled="!selectedMethod || isProcessing"
								:class="[
									'px-8 py-3 rounded-lg font-semibold transition',
									selectedMethod && !isProcessing
										? 'bg-primary-600 text-white hover:bg-primary-700'
										: 'bg-gray-300 text-gray-500 cursor-not-allowed',
								]"
							>
								<span v-if="!isProcessing">Thanh toán</span>
								<span v-else class="flex items-center">
									<svg
										class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
										fill="none"
										viewBox="0 0 24 24"
									>
										<circle
											class="opacity-25"
											cx="12"
											cy="12"
											r="10"
											stroke="currentColor"
											stroke-width="4"
										></circle>
										<path
											class="opacity-75"
											fill="currentColor"
											d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
										></path>
									</svg>
									Đang xử lý...
								</span>
							</button>
						</div>
					</div>

					<!-- Security Notice -->
					<div class="mt-4 p-4 bg-blue-50 rounded-lg">
						<div class="flex items-start">
							<svg
								class="w-5 h-5 text-blue-600 mt-0.5"
								fill="currentColor"
								viewBox="0 0 20 20"
							>
								<path
									fill-rule="evenodd"
									d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
									clip-rule="evenodd"
								></path>
							</svg>
							<div class="ml-3 text-sm text-blue-800">
								<p class="font-semibold">Thanh toán an toàn</p>
								<p>
									Thông tin thanh toán của bạn được mã hóa và
									bảo mật tuyệt đối.
								</p>
							</div>
						</div>
					</div>
				</div>

				<!-- Order Summary - 1 column -->
				<div class="lg:col-span-1">
					<div class="bg-white rounded-lg shadow-lg p-6 sticky top-4">
						<h3 class="text-lg font-bold mb-4">
							Thông tin đơn hàng
						</h3>

						<!-- Show Info -->
						<div class="mb-4 pb-4 border-b">
							<h4 class="font-semibold">{{ showInfo.name }}</h4>
							<p class="text-sm text-gray-600">
								{{ performanceInfo.date }}
							</p>
							<p class="text-sm text-gray-600">
								Suất: {{ performanceInfo.time }}
							</p>
						</div>

						<!-- Selected Seats -->
						<div class="mb-4 pb-4 border-b">
							<h4 class="font-semibold mb-3">Ghế đã chọn:</h4>
							<div class="space-y-2 max-h-40 overflow-y-auto">
								<div
									v-for="seat in selectedSeats"
									:key="seat.id"
									class="flex justify-between items-center text-sm"
								>
									<span>{{ seat.full_label }}</span>
									<!-- ← Thay đổi -->
									<span class="font-medium">{{
										formatPrice(seat.price)
									}}</span>
								</div>
							</div>
						</div>

						<!-- Price Details -->
						<div class="space-y-2 mb-4 pb-4 border-b">
							<div class="flex justify-between text-sm">
								<span>Tổng tiền vé:</span>
								<span>{{ formatPrice(subtotal) }}</span>
							</div>
							<div class="flex justify-between text-sm">
								<span>Phí dịch vụ:</span>
								<span>{{ formatPrice(serviceFee) }}</span>
							</div>
							<div
								v-if="discount > 0"
								class="flex justify-between text-sm text-green-600"
							>
								<span>Giảm giá:</span>
								<span>-{{ formatPrice(discount) }}</span>
							</div>
						</div>

						<!-- Total -->
						<div class="flex justify-between items-center mb-4">
							<span class="font-semibold">Tổng thanh toán:</span>
							<span class="text-xl font-bold text-primary-600">
								{{ formatPrice(totalAmount) }}
							</span>
						</div>

						<!-- Promo Code -->
						<div class="p-3 bg-gray-50 rounded-lg">
							<div class="flex space-x-2">
								<input
									v-model="promoCode"
									type="text"
									placeholder="Mã giảm giá"
									class="flex-1 px-3 py-2 border border-gray-300 rounded text-sm"
								/>
								<button
									@click="applyPromo"
									class="px-4 py-2 bg-gray-800 text-white rounded text-sm hover:bg-gray-700"
								>
									Áp dụng
								</button>
							</div>
						</div>

						<!-- Timer -->
						<div class="mt-4 p-3 bg-yellow-50 rounded-lg">
							<div class="text-sm text-yellow-800">
								⏱️ Thời gian giữ vé:
								<span class="font-bold">{{
									formatTime(timeLeft)
								}}</span>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</DefaultLayout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import DefaultLayout from "../layouts/DefaultLayout.vue";
import { useBookingStore } from "../stores/booking";

const router = useRouter();
const route = useRoute();
const bookingStore = useBookingStore();

// State
const selectedMethod = ref("");
const isProcessing = ref(false);
const promoCode = ref("");
const discount = ref(0);

const showInfo = ref({
	name: "",
});

const performanceInfo = ref({
	date: "",
	time: "",
});

const customerInfo = ref({});
const selectedSeats = ref([]);

// Timer
const timeLeft = ref(300); // 5 minutes
let timer = null;

// Computed
const subtotal = computed(() => {
	return selectedSeats.value.reduce((sum, seat) => sum + seat.price, 0);
});

const serviceFee = computed(() => {
	return selectedSeats.value.length * 10000;
});

const totalAmount = computed(() => {
	return subtotal.value + serviceFee.value - discount.value;
});

// Methods
const formatPrice = (price) => {
	return new Intl.NumberFormat("vi-VN", {
		style: "currency",
		currency: "VND",
	}).format(price);
};

const formatTime = (seconds) => {
	const mins = Math.floor(seconds / 60);
	const secs = seconds % 60;
	return `${mins}:${secs.toString().padStart(2, "0")}`;
};

const selectPaymentMethod = (method) => {
	selectedMethod.value = method;
};

const applyPromo = () => {
	// Mock promo code
	if (promoCode.value.toUpperCase() === "OPERA10") {
		discount.value = subtotal.value * 0.1; // 10% discount
		alert("Áp dụng mã giảm giá thành công!");
	} else {
		alert("Mã giảm giá không hợp lệ");
	}
};

const processPayment = async () => {

	if (!selectedMethod.value) return;
	isProcessing.value = true;

	try {
		// Create payment
		const paymentData = await bookingStore.processPayment(
			selectedMethod.value
		);

		console.log("Payment data:", paymentData);

		// Save booking data to sessionStorage before redirect/polling
		const bookingData = {
			showInfo: {
				name: showInfo.value.name,
			},
			performance: {
				date: performanceInfo.value.date,
				time: performanceInfo.value.time,
			},
			customerInfo: {
				fullName:
					customerInfo.value.fullName ||
					customerInfo.value.customer_name,
				email:
					customerInfo.value.email ||
					customerInfo.value.customer_email,
				phone:
					customerInfo.value.phone ||
					customerInfo.value.customer_phone,
			},
			amount: totalAmount.value,
			selectedSeats: selectedSeats.value,
			// Additional info
			bookingCode: bookingStore.bookingCode,
			status: "pending",
			transactionId: paymentData.transaction_id,
		};

		sessionStorage.setItem("bookingData", JSON.stringify(bookingData));

		// If VNPay or other payment methods that require redirect
		if (paymentData.payment_url) {
			console.log("Redirecting to:", paymentData.payment_url);
			// Redirect to payment gateway
			window.location.href = paymentData.payment_url;
			return;
		}

		// Handle mock or other payment types
		if (paymentData.auto_complete) {
			// Show waiting message for mock payment
			alert(
				`Đang xử lý thanh toán... Vui lòng đợi ${paymentData.wait_time} giây`
			);

			// Poll payment status
			const checkPayment = setInterval(async () => {
				try {
					const status = await bookingStore.checkPaymentStatus(
						paymentData.transaction_id
					);
					if (status.data.status === "success") {
						clearInterval(checkPayment);
						router.push(
							`/booking/confirmation/${status.data.booking_code}`
						);
					} else if (status.data.status === "failed") {
						clearInterval(checkPayment);
						alert("Thanh toán thất bại!");
						// Clear failed booking data
						sessionStorage.removeItem("bookingData");
					}
				} catch (error) {
					console.error("Error checking payment status:", error);
					clearInterval(checkPayment);
					alert("Lỗi kiểm tra trạng thái thanh toán");
				}
			}, 3000);
		}
	} catch (error) {
		console.error("Payment error:", error);
		alert("Lỗi thanh toán: " + error.message);
	} finally {
		isProcessing.value = false;
	}
};
const goBack = () => {
	router.back();
};

// Timer
const startTimer = () => {
	timer = setInterval(() => {
		if (timeLeft.value > 0) {
			timeLeft.value--;
		} else {
			clearInterval(timer);
			alert("Hết thời gian giữ vé. Vui lòng đặt lại.");
			router.push("/");
		}
	}, 1000);
};

onMounted(() => {
	// Load show and performance data
	if (bookingStore.selectedPerformance) {
		const performance = bookingStore.selectedPerformance;
		showInfo.value = {
			name: performance.show_name || performance.show?.name,
		};
		performanceInfo.value = {
			date: new Date(performance.datetime).toLocaleDateString("vi-VN"),
			time: new Date(performance.datetime).toLocaleTimeString("vi-VN", {
				hour: "2-digit",
				minute: "2-digit",
			}),
		};
	}

	// Load selected seats from store instead of mock data
	if (bookingStore.selectedSeats && bookingStore.selectedSeats.length > 0) {
		selectedSeats.value = bookingStore.selectedSeats;
	} else {
		// Redirect back if no seats selected
		alert("Không tìm thấy ghế đã chọn. Vui lòng chọn lại.");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	startTimer();
});

onUnmounted(() => {
	if (timer) {
		clearInterval(timer);
	}
});
</script>
