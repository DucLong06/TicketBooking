<template>
	<DefaultLayout>
		<div class="container mx-auto px-4 py-8">
			<!-- Breadcrumb - giữ nguyên -->
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
					<li>
						<router-link
							:to="`/booking/${$route.params.showId}`"
							class="text-gray-500 hover:text-primary-600"
						>
							Chọn suất diễn
						</router-link>
					</li>
					<li class="text-gray-400">/</li>
					<li>
						<router-link
							:to="`/booking/${$route.params.showId}/seats`"
							class="text-gray-500 hover:text-primary-600"
						>
							Chọn ghế
						</router-link>
					</li>
					<li class="text-gray-400">/</li>
					<li class="text-gray-700 font-medium">
						Thông tin khách hàng
					</li>
				</ol>
			</nav>

			<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
				<!-- Form Section - 2 columns -->
				<div class="lg:col-span-2">
					<div
						class="bg-white rounded-lg shadow-lg p-6 mb-20 lg:mb-0"
					>
						<h2 class="text-2xl font-bold mb-6">
							Thông tin người đặt vé
						</h2>

						<form @submit.prevent="handleSubmit">
							<div class="mb-4">
								<label
									class="block text-sm font-medium text-gray-700 mb-2"
								>
									Họ và tên
									<span class="text-red-500">*</span>
								</label>
								<input
									v-model="customerInfo.fullName"
									type="text"
									required
									class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
									placeholder="Nguyễn Văn A"
								/>
								<p
									v-if="errors.fullName"
									class="mt-1 text-sm text-red-500"
								>
									{{ errors.fullName }}
								</p>
							</div>

							<!-- Email -->
							<div class="mb-4">
								<label
									class="block text-sm font-medium text-gray-700 mb-2"
								>
									Email <span class="text-red-500">*</span>
								</label>
								<input
									v-model="customerInfo.email"
									type="email"
									required
									class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
									placeholder="example@email.com"
								/>
								<p class="mt-1 text-xs text-gray-500">
									{{ emailDescription }}
								</p>
								<p
									v-if="errors.email"
									class="mt-1 text-sm text-red-500"
								>
									{{ errors.email }}
								</p>
							</div>

							<div class="mb-4">
								<label
									class="block text-sm font-medium text-gray-700 mb-2"
								>
									Số điện thoại
									<span class="text-red-500">*</span>
								</label>
								<input
									v-model="customerInfo.phone"
									type="tel"
									required
									class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
									placeholder="0912345678"
								/>
								<p
									v-if="errors.phone"
									class="mt-1 text-sm text-red-500"
								>
									{{ errors.phone }}
								</p>
							</div>

							<!-- Địa chỉ -->
							<div class="mb-4">
								<label
									class="block text-sm font-medium text-gray-700 mb-2"
								>
									Địa chỉ <span class="text-red-500">*</span>
								</label>
								<textarea
									v-model="customerInfo.address"
									required
									rows="3"
									class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
									placeholder="Nhập địa chỉ nhận vé..."
								></textarea>
								<p class="mt-1 text-xs text-gray-500">
									{{ addressDescription }}
								</p>
								<p
									v-if="errors.address"
									class="mt-1 text-sm text-red-500"
								>
									{{ errors.address }}
								</p>
							</div>

							<!-- Thời gian ship vé -->
							<div class="mb-6">
								<label
									class="block text-sm font-medium text-gray-700 mb-2"
								>
									Thời gian ship vé
									<span class="text-red-500">*</span>
								</label>
								<select
									v-model="customerInfo.shippingTime"
									required
									class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
								>
									<option value="business_hours">
										Trong giờ hành chính
									</option>
									<option value="after_hours">
										Ngoài giờ hành chính
									</option>
								</select>
							</div>

							<!-- Ghi chú -->
							<div class="mb-6">
								<label
									class="block text-sm font-medium text-gray-700 mb-2"
								>
									Ghi chú
								</label>
								<textarea
									v-model="customerInfo.notes"
									rows="3"
									class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
									placeholder="Yêu cầu đặc biệt (nếu có)..."
								></textarea>
							</div>

							<!-- Buttons cho desktop -->
							<div class="hidden lg:flex justify-between">
								<button
									type="button"
									@click="goBack"
									class="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition"
								>
									← Quay lại
								</button>
								<button
									type="submit"
									class="px-8 py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition"
								>
									Tiếp tục thanh toán →
								</button>
							</div>
						</form>
					</div>
				</div>

				<!-- Order Summary - Desktop only (1 column) -->
				<div class="hidden lg:block lg:col-span-1">
					<div class="bg-white rounded-lg shadow-lg p-6 sticky top-4">
						<h3 class="text-xl font-bold mb-4">Tóm tắt đơn hàng</h3>

						<!-- Show Info -->
						<div class="mb-4 pb-4 border-b">
							<h4 class="font-semibold mb-2">
								{{ showInfo.name }}
							</h4>
							<p class="text-sm text-gray-600">
								{{ performanceInfo.date }} -
								{{ performanceInfo.time }}
							</p>
						</div>

						<!-- Selected Seats -->
						<div class="mb-4 pb-4 border-b">
							<h4 class="font-semibold mb-2">Ghế đã chọn</h4>
							<div class="space-y-2">
								<div
									v-for="seat in selectedSeats"
									:key="seat.id"
									class="flex justify-between text-sm"
								>
									<span
										>{{ seat.full_label }} -
										{{ seat.section_name }}</span
									>
									<span class="font-semibold">{{
										formatPrice(seat.price)
									}}</span>
								</div>
							</div>
						</div>

						<!-- Price Breakdown -->
						<div class="space-y-2 mb-4 pb-4 border-b">
							<div class="flex justify-between text-sm">
								<span class="text-gray-600">Tổng tiền vé:</span>
								<span class="font-semibold">{{
									formatPrice(ticketAmount)
								}}</span>
							</div>

							<div class="flex justify-between text-sm">
								<span class="text-gray-600"
									>Phí vận chuyển:</span
								>
								<span class="font-semibold text-primary-600">{{
									formatPrice(serviceFee)
								}}</span>
							</div>
						</div>

						<!-- Total Amount -->
						<div
							class="flex justify-between items-center text-lg font-bold mb-6"
						>
							<span>Tổng thanh toán:</span>
							<span class="text-primary-600">{{
								formatPrice(totalAmount)
							}}</span>
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

			<!-- Mobile Sticky Bottom Bar -->
			<div
				class="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg z-50"
			>
				<div class="px-4 py-3">
					<!-- Tổng thanh toán -->
					<div class="flex justify-between items-center mb-3">
						<div>
							<p class="text-xs text-gray-500">Tổng thanh toán</p>
							<p class="text-lg font-bold text-primary-600">
								{{ formatPrice(totalAmount) }}
							</p>
						</div>
						<div class="text-right">
							<p class="text-xs text-gray-500">
								⏱️ {{ formatTime(timeLeft) }}
							</p>
							<button
								@click="toggleOrderSummary"
								class="text-xs text-primary-600 hover:text-primary-700 underline"
							>
								{{
									showOrderSummary
										? "Ẩn chi tiết"
										: "Xem chi tiết"
								}}
							</button>
						</div>
					</div>

					<div
						v-show="showOrderSummary"
						class="mb-3 p-3 bg-gray-50 rounded-lg text-sm max-h-48 overflow-y-auto"
					>
						<div class="space-y-2">
							<div class="flex justify-between">
								<span class="text-gray-600">Tiền vé:</span>
								<span class="font-semibold">{{
									formatPrice(ticketAmount)
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600"
									>Phí vận chuyển:</span
								>
								<span class="font-semibold">{{
									formatPrice(serviceFee)
								}}</span>
							</div>
							<div class="border-t pt-2 mt-2">
								<p class="text-xs text-gray-500 mb-1">
									Ghế:
									<span
										v-for="(seat, index) in selectedSeats"
										:key="seat.id"
									>
										{{ seat.full_label }} -
										{{ seat.section_name
										}}<span
											v-if="
												index < selectedSeats.length - 1
											"
											>,
										</span>
									</span>
								</p>
							</div>
						</div>
					</div>

					<!-- Buttons -->
					<div class="flex gap-2">
						<button
							type="button"
							@click="goBack"
							class="flex-1 px-4 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition font-medium"
						>
							← Quay lại
						</button>
						<button
							@click="handleSubmit"
							class="flex-1 px-4 py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition"
						>
							Thanh toán →
						</button>
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
import { useToast } from "vue-toastification";

const toast = useToast();
const bookingStore = useBookingStore();
const router = useRouter();
const route = useRoute();

// Form data
const showInfo = ref({
	name: "",
	service_fee_per_ticket: 10000, // default
});

const performanceInfo = ref({
	date: "",
	time: "",
});

const customerInfo = ref({
	fullName: "",
	email: "",
	phone: "",
	idNumber: "",
	address: "",
	notes: "",
	shippingTime: "business_hours",
});

const agreedToTerms = ref(false);
const errors = ref({});
const addressDescription = ref(
	"Địa chỉ nhận vé cứng. Nhà hát Hồ Gươm chỉ sử dụng vé cứng để vào cửa."
);
const emailDescription = ref(
	"Email để nhận xác nhận thanh toán hoặc xác nhận đặt vé"
);

const selectedSeats = ref([]);

// Mobile order summary toggle
const showOrderSummary = ref(false);

const toggleOrderSummary = () => {
	showOrderSummary.value = !showOrderSummary.value;
};

// Timer
const timeLeft = ref(600); // 10 minutes
let timer = null;

const serviceFeePerTicket = computed(() => {
	if (showInfo.value.service_fee_per_ticket) {
		return showInfo.value.service_fee_per_ticket;
	}
	if (bookingStore.currentShow?.service_fee_per_ticket) {
		return bookingStore.currentShow.service_fee_per_ticket;
	}
	// Default 10,000đ
	return 10000;
});

const ticketAmount = computed(() => {
	return selectedSeats.value.reduce((sum, seat) => sum + seat.price, 0);
});

const serviceFee = computed(() => {
	return selectedSeats.value.length * serviceFeePerTicket.value;
});

const totalAmount = computed(() => {
	return ticketAmount.value + serviceFee.value;
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

const validateForm = () => {
	errors.value = {};

	if (!customerInfo.value.fullName.trim()) {
		errors.value.fullName = "Vui lòng nhập họ tên";
	}

	const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	if (!emailRegex.test(customerInfo.value.email)) {
		errors.value.email = "Email không hợp lệ";
	}

	const phoneRegex = /^(0[3|5|7|8|9])+([0-9]{8})$/;
	if (!phoneRegex.test(customerInfo.value.phone)) {
		errors.value.phone = "Số điện thoại không hợp lệ";
	}

	if (!customerInfo.value.address.trim()) {
		errors.value.address = "Vui lòng nhập địa chỉ";
	}

	return Object.keys(errors.value).length === 0;
};

const handleSubmit = async () => {
	if (!validateForm()) return;

	try {
		bookingStore.customerInfo = {
			customer_name: customerInfo.value.fullName,
			customer_email: customerInfo.value.email,
			customer_phone: customerInfo.value.phone,
			customer_address: customerInfo.value.address,
			shipping_time: customerInfo.value.shippingTime,
			notes: customerInfo.value.notes || "",
		};

		const booking = await bookingStore.createBooking();
		const paymentData = await bookingStore.processPayment("9pay");

		const bookingData = {
			showInfo: {
				name: showInfo.value.name,
			},
			performance: {
				date: performanceInfo.value.date,
				time: performanceInfo.value.time,
			},
			customerInfo: {
				fullName: customerInfo.value.fullName,
				email: customerInfo.value.email,
				phone: customerInfo.value.phone,
			},
			amount: totalAmount.value,
			ticketAmount: ticketAmount.value,
			serviceFee: serviceFee.value,
			selectedSeats: selectedSeats.value,
			bookingCode: bookingStore.bookingCode,
			status: "pending",
			transactionId: paymentData.transaction_id,
		};

		sessionStorage.setItem("bookingData", JSON.stringify(bookingData));

		if (paymentData.payment_url) {
			window.location.href = paymentData.payment_url;
		} else {
			throw new Error("Không nhận được URL thanh toán từ 9Pay");
		}
	} catch (error) {
		console.error("Error:", error);
		toast.error("Lỗi: " + (error.response?.data?.error || error.message));
	}
};

const goBack = () => {
	router.back();
};

const startTimer = () => {
	const savedExpiry = sessionStorage.getItem("reservationExpiry");

	if (!savedExpiry) {
		alert("Không tìm thấy thông tin đặt vé. Vui lòng chọn lại.");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	const expiryDate = new Date(savedExpiry);

	const now = new Date();
	if (expiryDate <= now) {
		alert("Hết thời gian giữ ghế. Vui lòng đặt lại.");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	timer = setInterval(() => {
		const now = new Date();
		const diff = Math.floor((expiryDate - now) / 1000);
		timeLeft.value = Math.max(0, diff);

		if (timeLeft.value === 0) {
			clearInterval(timer);
			alert("Hết thời gian giữ ghế. Vui lòng đặt lại.");
			router.push("/");
		}
	}, 1000);
};

onMounted(() => {
	// Load từ bookingStore trước (ưu tiên)
	if (bookingStore.currentShow) {
		showInfo.value = {
			name: bookingStore.currentShow.name,
			service_fee_per_ticket:
				bookingStore.currentShow.service_fee_per_ticket || 10000,
		};
	}

	// Load performance data
	if (bookingStore.selectedPerformance) {
		const performance = bookingStore.selectedPerformance;
		if (!showInfo.value.name) {
			showInfo.value.name =
				performance.show_name || performance.show?.name;
		}
		performanceInfo.value = {
			date: new Date(performance.datetime).toLocaleDateString("vi-VN"),
			time: new Date(performance.datetime).toLocaleTimeString("vi-VN", {
				hour: "2-digit",
				minute: "2-digit",
			}),
		};
	} else {
		// Fallback: Load từ sessionStorage
		const savedPerformance = sessionStorage.getItem("selectedPerformance");
		if (savedPerformance) {
			const performance = JSON.parse(savedPerformance);
			if (!showInfo.value.name) {
				showInfo.value.name = performance.show_name;
			}
			performanceInfo.value = {
				date: new Date(performance.datetime).toLocaleDateString(
					"vi-VN"
				),
				time: new Date(performance.datetime).toLocaleTimeString(
					"vi-VN",
					{
						hour: "2-digit",
						minute: "2-digit",
					}
				),
			};
		}
	}

	// Load selected seats
	if (bookingStore.selectedSeats?.length > 0) {
		selectedSeats.value = bookingStore.selectedSeats;
	} else {
		const savedSeats = sessionStorage.getItem("selectedSeats");
		if (savedSeats) {
			selectedSeats.value = JSON.parse(savedSeats);
		} else {
			alert("Không tìm thấy ghế đã chọn. Vui lòng chọn lại.");
			router.push(`/booking/${route.params.showId}/seats`);
			return;
		}
	}

	startTimer();
});

onUnmounted(() => {
	if (timer) {
		clearInterval(timer);
	}
});
</script>
