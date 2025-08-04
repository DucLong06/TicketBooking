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
					<div class="bg-white rounded-lg shadow-lg p-6">
						<h2 class="text-2xl font-bold mb-6">
							Thông tin người đặt vé
						</h2>

						<form @submit.prevent="handleSubmit">
							<!-- Full Name -->
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
									Vé điện tử sẽ được gửi đến email này
								</p>
								<p
									v-if="errors.email"
									class="mt-1 text-sm text-red-500"
								>
									{{ errors.email }}
								</p>
							</div>

							<!-- Phone -->
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

							<!-- ID Number -->
							<div class="mb-4">
								<label
									class="block text-sm font-medium text-gray-700 mb-2"
								>
									CMND/CCCD
								</label>
								<input
									v-model="customerInfo.idNumber"
									type="text"
									class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
									placeholder="001234567890"
								/>
							</div>

							<!-- Notes -->
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

							<!-- Terms & Conditions -->
							<div class="mb-6">
								<label class="flex items-start">
									<input
										v-model="agreedToTerms"
										type="checkbox"
										required
										class="mt-1 mr-2"
									/>
									<span class="text-sm text-gray-600">
										Tôi đồng ý với
										<a
											href="#"
											class="text-primary-600 hover:underline"
											>điều khoản sử dụng</a
										>
										và
										<a
											href="#"
											class="text-primary-600 hover:underline"
											>chính sách bảo mật</a
										>
										<span class="text-red-500">*</span>
									</span>
								</label>
							</div>

							<!-- Newsletter -->
							<div class="mb-6 p-4 bg-gray-50 rounded-lg">
								<label class="flex items-start">
									<input
										v-model="subscribeNewsletter"
										type="checkbox"
										class="mt-1 mr-2"
									/>
									<span class="text-sm text-gray-600">
										Nhận thông tin ưu đãi và chương trình
										mới qua email
									</span>
								</label>
							</div>

							<!-- Buttons -->
							<div class="flex justify-between">
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
							<div class="space-y-2 max-h-60 overflow-y-auto">
								<div
									v-for="seat in selectedSeats"
									:key="seat.id"
									class="flex justify-between items-center text-sm p-2 bg-gray-50 rounded"
								>
									<div>
										<span class="font-medium"
											>{{ seat.row
											}}{{ seat.number }}</span
										>
										<span
											class="text-gray-500 ml-2 text-xs"
											>{{ seat.sectionName }}</span
										>
									</div>
									<span class="font-semibold">{{
										formatPrice(seat.price)
									}}</span>
								</div>
							</div>
						</div>

						<!-- Price Breakdown -->
						<div class="space-y-2 mb-4 pb-4 border-b">
							<div class="flex justify-between text-sm">
								<span>Tổng tiền vé:</span>
								<span>{{ formatPrice(subtotal) }}</span>
							</div>
							<div class="flex justify-between text-sm">
								<span>Phí dịch vụ:</span>
								<span>{{ formatPrice(serviceFee) }}</span>
							</div>
						</div>

						<!-- Total -->
						<div class="flex justify-between items-center">
							<span class="font-semibold">Tổng thanh toán:</span>
							<span class="text-xl font-bold text-primary-600">
								{{ formatPrice(totalAmount) }}
							</span>
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

const bookingStore = useBookingStore();
const router = useRouter();
const route = useRoute();

// Form data
const customerInfo = ref({
	fullName: "",
	email: "",
	phone: "",
	idNumber: "",
	notes: "",
});

const agreedToTerms = ref(false);
const subscribeNewsletter = ref(false);
const errors = ref({});

// Mock data - sẽ lấy từ sessionStorage/store
const showInfo = ref({
	name: "Italia Mistero",
});

const performanceInfo = ref({
	date: "15/12/2024",
	time: "19:00",
});

const selectedSeats = ref([]);

// Timer
const timeLeft = ref(600); // 10 minutes
let timer = null;

// Computed
const subtotal = computed(() => {
	return selectedSeats.value.reduce((sum, seat) => sum + seat.price, 0);
});

const serviceFee = computed(() => {
	return selectedSeats.value.length * 10000; // 10k per ticket
});

const totalAmount = computed(() => {
	return subtotal.value + serviceFee.value;
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

	// Validate name
	if (!customerInfo.value.fullName.trim()) {
		errors.value.fullName = "Vui lòng nhập họ tên";
	}

	// Validate email
	const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
	if (!emailRegex.test(customerInfo.value.email)) {
		errors.value.email = "Email không hợp lệ";
	}

	// Validate phone
	const phoneRegex = /^(0[3|5|7|8|9])+([0-9]{8})$/;
	if (!phoneRegex.test(customerInfo.value.phone)) {
		errors.value.phone = "Số điện thoại không hợp lệ";
	}

	return Object.keys(errors.value).length === 0;
};

const handleSubmit = async () => {
	if (!validateForm()) return;

	if (!agreedToTerms.value) {
		alert("Vui lòng đồng ý với điều khoản sử dụng");
		return;
	}

	try {
		bookingStore.customerInfo = {
			customer_name: customerInfo.value.fullName, // fullName → customer_name
			customer_email: customerInfo.value.email, // email → customer_email
			customer_phone: customerInfo.value.phone, // phone → customer_phone
			customer_id_number: customerInfo.value.idNumber, // idNumber → customer_id_number
			notes: customerInfo.value.notes || "",
		};
		const booking = await bookingStore.createBooking();

		// Navigate to payment
		router.push(`/booking/${route.params.showId}/payment`);
	} catch (error) {
		alert("Lỗi khi tạo đơn đặt vé: " + error.message);
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
	// Load selected seats from sessionStorage
	const savedSeats = sessionStorage.getItem("selectedSeats");
	if (savedSeats) {
		selectedSeats.value = JSON.parse(savedSeats);
	} else {
		// Mock data for testing
		selectedSeats.value = [
			{
				id: "A-5",
				row: "A",
				number: 5,
				sectionName: "Khu A - VIP",
				price: 2000000,
			},
			{
				id: "A-6",
				row: "A",
				number: 6,
				sectionName: "Khu A - VIP",
				price: 2000000,
			},
		];
	}

	// Load performance info
	const savedPerformance = sessionStorage.getItem("selectedPerformance");
	if (savedPerformance) {
		const data = JSON.parse(savedPerformance);
		performanceInfo.value.date = new Date(data.date).toLocaleDateString(
			"vi-VN"
		);
		performanceInfo.value.time = data.time;
	}

	startTimer();
});

onUnmounted(() => {
	if (timer) {
		clearInterval(timer);
	}
});
</script>
