<template>
	<DefaultLayout>
		<div class="container mx-auto px-4 py-8">
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

				<div class="hidden lg:block lg:col-span-1">
					<div class="bg-white rounded-lg shadow-lg p-6 sticky top-4">
						<h3 class="text-xl font-bold mb-4">Tóm tắt đơn hàng</h3>

						<div class="mb-4 pb-4 border-b">
							<h4 class="font-semibold mb-2">
								{{ showInfo.name }}
							</h4>
							<p class="text-sm text-gray-600">
								{{ performanceInfo.date }} -
								{{ performanceInfo.time }}
							</p>
						</div>

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
						<div class="mb-4 pb-4 border-b">
							<label
								class="block text-sm font-medium text-gray-700 mb-2"
								>Mã giảm giá</label
							>
							<div class="flex gap-2">
								<input
									v-model="discountCodeInput"
									type="text"
									class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
									placeholder="Nhập mã giảm giá"
									:disabled="bookingStore.isDiscountSuccess"
								/>
								<button
									@click="applyDiscountCode"
									:disabled="bookingStore.isDiscountSuccess"
									class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
								>
									Áp dụng
								</button>
							</div>
							<p
								v-if="bookingStore.discountMessage"
								class="mt-2 text-sm"
								:class="{
									'text-green-600':
										bookingStore.isDiscountSuccess,
									'text-red-500':
										!bookingStore.isDiscountSuccess,
								}"
							>
								{{ bookingStore.discountMessage }}
							</p>
						</div>

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
								<span class="font-semibold text-primary-600">
									{{ formatPrice(shippingFee) }}
								</span>
							</div>
							<div class="flex justify-between text-sm">
								<span class="text-gray-600">Phí dịch vụ:</span>
								<span class="font-semibold text-primary-600">{{
									formatPrice(serviceFee)
								}}</span>
							</div>
							<div
								v-if="bookingStore.discountAmount > 0"
								class="flex justify-between text-sm"
							>
								<span class="text-gray-600">Giảm giá:</span>
								<span class="font-semibold text-green-600"
									>-{{
										formatPrice(bookingStore.discountAmount)
									}}</span
								>
							</div>
						</div>

						<div
							class="flex justify-between items-center text-lg font-bold mb-6"
						>
							<span>Tổng thanh toán:</span>
							<span class="text-primary-600">{{
								formatPrice(finalAmount)
							}}</span>
						</div>

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

			<div
				class="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg z-50"
			>
				<div class="px-4 py-3">
					<div class="flex justify-between items-center mb-3">
						<div>
							<p class="text-xs text-gray-500">Tổng thanh toán</p>
							<p class="text-lg font-bold text-primary-600">
								{{ formatPrice(finalAmount) }}
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
								<span class="text-gray-600">Phí dịch vụ:</span>
								<span class="font-semibold">{{
									formatPrice(serviceFee)
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600"
									>Phí vận chuyển:</span
								>
								<span class="font-semibold">{{
									formatPrice(shippingFee)
								}}</span>
							</div>
							<div
								v-if="bookingStore.discountAmount > 0"
								class="flex justify-between"
							>
								<span class="text-gray-600">Giảm giá:</span>
								<span class="font-semibold text-green-600"
									>-{{
										formatPrice(bookingStore.discountAmount)
									}}</span
								>
							</div>
							<div class="pt-2 border-t">
								<label
									class="block text-xs font-medium text-gray-700 mb-1"
									>Mã giảm giá</label
								>
								<div class="flex gap-2">
									<input
										v-model="discountCodeInput"
										type="text"
										class="w-full px-2 py-1 text-sm border border-gray-300 rounded-md focus:ring-1 focus:ring-primary-500"
										placeholder="Nhập mã"
										:disabled="
											bookingStore.isDiscountSuccess
										"
									/>
									<button
										@click="applyDiscountCode"
										:disabled="
											bookingStore.isDiscountSuccess
										"
										class="px-3 py-1 bg-primary-600 text-white rounded-md text-xs hover:bg-primary-700 disabled:bg-gray-400"
									>
										Áp dụng
									</button>
								</div>
								<p
									v-if="bookingStore.discountMessage"
									class="mt-1 text-xs"
									:class="{
										'text-green-600':
											bookingStore.isDiscountSuccess,
										'text-red-500':
											!bookingStore.isDiscountSuccess,
									}"
								>
									{{ bookingStore.discountMessage }}
								</p>
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
	service_fee_per_ticket: 0, // default
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
const shippingFee = computed(() => {
	return bookingStore.shippingFee || 30000;
});
const selectedSeats = ref([]);

// Mobile order summary toggle
const showOrderSummary = ref(false);

const toggleOrderSummary = () => {
	showOrderSummary.value = !showOrderSummary.value;
};

// Timer
const timeLeft = ref(600);
let timer = null;

const serviceFeePerTicket = computed(() => {
	if (showInfo.value.service_fee_per_ticket) {
		return showInfo.value.service_fee_per_ticket;
	}

	if (bookingStore.currentShow?.service_fee_per_ticket) {
		return bookingStore.currentShow.service_fee_per_ticket;
	}

	try {
		const savedPerformance = sessionStorage.getItem("selectedPerformance");
		if (savedPerformance) {
			const performance = JSON.parse(savedPerformance);
			if (performance.service_fee_per_ticket) {
				return performance.service_fee_per_ticket;
			}
		}
	} catch (error) {
		console.error("Error parsing savedPerformance:", error);
	}

	return 0;
});

const ticketAmount = computed(() => {
	return selectedSeats.value.reduce(
		(sum, seat) => sum + (seat.price || 0),
		0
	);
});

const serviceFee = computed(() => {
	if (!serviceFeePerTicket.value) return 0;
	return selectedSeats.value.length * serviceFeePerTicket.value;
});

const totalAmount = computed(() => {
	return ticketAmount.value + serviceFee.value + shippingFee.value;
});

const finalAmount = computed(() => {
	if (bookingStore.currentBooking?.final_amount) {
		return bookingStore.currentBooking.final_amount;
	}
	return totalAmount.value;
});
// Discount
const discountCodeInput = ref("");

const applyDiscountCode = async () => {
	if (!discountCodeInput.value.trim()) {
		toast.warning("Vui lòng nhập mã giảm giá.");
		return;
	}
	await bookingStore.applyDiscount(
		discountCodeInput.value,
		customerInfo.value
	);
};

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
			discount_code: bookingStore.isDiscountSuccess
				? discountCodeInput.value
				: "",
		};

		const booking = await bookingStore.createBooking();
		if (
			!booking.seat_reservations ||
			booking.seat_reservations.length === 0
		) {
			toast.error("Lỗi: Không có ghế. Vui lòng chọn lại.");
			bookingStore.clearBooking();
			router.push(`/booking/${route.params.showId}`);
			return;
		}

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
			amount: finalAmount.value,
			ticketAmount: ticketAmount.value,
			serviceFee: serviceFee.value,
			discountAmount: bookingStore.discountAmount,
			selectedSeats: selectedSeats.value,
			bookingCode: bookingStore.bookingCode,
			status: "pending",
			transactionId: paymentData.transaction_id,
		};

		sessionStorage.setItem("bookingData", JSON.stringify(bookingData));

		// Redirect to payment
		if (paymentData.payment_url) {
			window.location.href = paymentData.payment_url;
		} else {
			throw new Error("Không nhận được URL thanh toán từ 9Pay");
		}
	} catch (error) {
		console.error("Error:", error);
		bookingStore.clearBooking();
		toast.error(error.message || "Có lỗi. Vui lòng chọn lại.");

		if (error.shouldRedirect) {
			setTimeout(() => {
				router.push(`/booking/${route.params.showId}`);
			}, 1500);
		}
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
	console.log("🚀 [CustomerInfo] Validating data...");

	bookingStore.resetDiscount();
	discountCodeInput.value = "";

	const existingSessionId = sessionStorage.getItem("session_id");
	if (existingSessionId) {
		bookingStore.sessionId = existingSessionId;
		console.log("✅ Session ID restored:", existingSessionId);
	} else {
		console.error("❌ No session ID found");
		toast.warning("Phiên đã hết hạn. Vui lòng chọn lại ghế.");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	let hasSeats = false;

	if (bookingStore.selectedSeats?.length > 0) {
		selectedSeats.value = bookingStore.selectedSeats;
		hasSeats = true;
		console.log("✅ Seats from store:", selectedSeats.value.length);
	} else {
		const savedSeats = sessionStorage.getItem("selectedSeats");
		if (savedSeats) {
			try {
				const parsedSeats = JSON.parse(savedSeats);
				selectedSeats.value = parsedSeats;

				bookingStore.selectedSeats = parsedSeats;

				hasSeats = parsedSeats.length > 0;
				console.log(
					"✅ Seats from sessionStorage and restored to store:",
					parsedSeats.length
				);
			} catch (e) {
				console.error("Failed to parse savedSeats:", e);
			}
		}
	}

	if (!hasSeats) {
		console.error("❌ No seats found");
		toast.warning("Vui lòng chọn ghế trước");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	const savedPerformance = sessionStorage.getItem("selectedPerformance");
	if (savedPerformance) {
		try {
			const performance = JSON.parse(savedPerformance);

			if (
				!bookingStore.selectedPerformance ||
				!bookingStore.selectedPerformance.id
			) {
				bookingStore.selectedPerformance = performance;
				console.log(
					"✅ Restored selectedPerformance to store:",
					performance.id
				);
			}

			showInfo.value = {
				name:
					performance.show_name ||
					bookingStore.currentShow?.name ||
					"",
				service_fee_per_ticket:
					performance.service_fee_per_ticket ||
					bookingStore.currentShow?.service_fee_per_ticket,
			};

			if (performance.datetime) {
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
		} catch (e) {
			console.error("Failed to parse savedPerformance:", e);
		}
	} else if (bookingStore.currentShow) {
		// Fallback to store
		showInfo.value = {
			name: bookingStore.currentShow.name,
			service_fee_per_ticket:
				bookingStore.currentShow.service_fee_per_ticket,
		};
	}

	if (!showInfo.value.name || !performanceInfo.value.date) {
		console.error("❌ Missing show or performance info");
		toast.warning("Thiếu thông tin suất diễn. Vui lòng chọn lại.");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	if (!serviceFeePerTicket.value) {
		console.error("❌ Service fee not found");
		toast.warning("Thiếu thông tin phí dịch vụ. Vui lòng chọn lại ghế.");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	const savedExpiry = sessionStorage.getItem("reservationExpiry");
	if (!savedExpiry) {
		console.error("❌ No reservation expiry");
		toast.warning("Phiên đã hết hạn. Vui lòng chọn lại ghế.");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	const expiryDate = new Date(savedExpiry);
	const now = new Date();
	if (expiryDate <= now) {
		console.error("❌ Reservation expired");
		toast.warning("Hết thời gian giữ ghế. Vui lòng chọn lại.");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	// Start timer
	timer = setInterval(() => {
		const now = new Date();
		const diff = Math.floor((expiryDate - now) / 1000);
		timeLeft.value = Math.max(0, diff);

		if (timeLeft.value === 0) {
			clearInterval(timer);
			toast.error("Hết thời gian giữ ghế");
			router.push(`/booking/${route.params.showId}/seats`);
		}
	}, 1000);
});

onUnmounted(() => {
	if (timer) {
		clearInterval(timer);
	}
	discountCodeInput.value = "";
});
</script>
