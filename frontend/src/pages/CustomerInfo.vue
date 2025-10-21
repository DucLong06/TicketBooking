<template>
	<DefaultLayout>
		<div class="container mx-auto px-4 py-8">
			<nav class="mb-6">
				<ol class="uppercase flex items-center space-x-2 text-sm">
					<li>
						<router-link
							to="/"
							class="text-[#d8a669] hover:text-[#b8884d] font-medium transition"
						>
							Trang chủ
						</router-link>
					</li>
					<li class="text-[#a0866b]">/</li>
					<li>
						<router-link
							:to="`/booking/${$route.params.showId}`"
							class="text-[#d8a669] hover:text-[#b8884d] font-medium transition"
						>
							Chọn suất diễn
						</router-link>
					</li>
					<li class="text-[#a0866b]">/</li>
					<li>
						<router-link
							:to="`/booking/${$route.params.showId}/seats`"
							class="text-[#d8a669] hover:text-[#b8884d] font-medium transition"
						>
							Chọn ghế
						</router-link>
					</li>
					<li class="text-[#a0866b]">/</li>
					<li class="text-[#372e2d] font-semibold">
						Thông tin khách hàng
					</li>
				</ol>
			</nav>

			<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
				<div class="lg:col-span-2">
					<div
						class="uppercase bg-[#fdfcf0] border border-[#d8a669]/30 rounded-lg shadow-lg p-6 mb-20 lg:mb-0"
					>
						<h2 class="text-2xl font-bold mb-6 text-[#372e2d]">
							Thông tin người đặt vé
						</h2>

						<form @submit.prevent="handleSubmit">
							<div class="mb-4">
								<label
									class="block text-sm font-medium text-[#372e2d] mb-2"
								>
									Họ và tên
									<span class="text-red-500">*</span>
								</label>
								<input
									v-model="customerInfo.fullName"
									type="text"
									required
									class="w-full px-4 py-2 border border-[#d8a669]/50 rounded-lg focus:ring-2 focus:ring-[#d8a669] focus:border-[#d8a669] bg-white text-[#372e2d]"
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
									class="block text-sm font-medium text-[#372e2d] mb-2"
								>
									Email <span class="text-red-500">*</span>
								</label>
								<input
									v-model="customerInfo.email"
									type="email"
									required
									class="w-full px-4 py-2 border border-[#d8a669]/50 rounded-lg focus:ring-2 focus:ring-[#d8a669] focus:border-[#d8a669] bg-white text-[#372e2d]"
									placeholder="example@email.com"
								/>
								<p
									class="mt-1 lowercase text-xs text-[#372e2d]/70"
								>
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
									class="block text-sm font-medium text-[#372e2d] mb-2"
								>
									Số điện thoại
									<span class="text-red-500">*</span>
								</label>
								<input
									v-model="customerInfo.phone"
									type="tel"
									required
									class="w-full px-4 py-2 border border-[#d8a669]/50 rounded-lg focus:ring-2 focus:ring-[#d8a669] focus:border-[#d8a669] bg-white text-[#372e2d]"
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
									class="block text-sm font-medium text-[#372e2d] mb-2"
								>
									Địa chỉ <span class="text-red-500">*</span>
								</label>
								<textarea
									v-model="customerInfo.address"
									required
									rows="3"
									class="w-full px-4 py-2 border border-[#d8a669]/50 rounded-lg focus:ring-2 focus:ring-[#d8a669] focus:border-[#d8a669] bg-white text-[#372e2d]"
									placeholder="Nhập địa chỉ nhận vé..."
								></textarea>
								<p
									class="lowercase mt-1 text-xs text-[#372e2d]/70"
								>
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
									class="block text-sm font-medium text-[#372e2d] mb-2"
								>
									Thời gian ship vé
									<span class="text-red-500">*</span>
								</label>
								<select
									v-model="customerInfo.shippingTime"
									required
									class="w-full px-4 py-2 border border-[#d8a669]/50 rounded-lg focus:ring-2 focus:ring-[#d8a669] focus:border-[#d8a669] bg-white text-[#372e2d]"
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
									class="block text-sm font-medium text-[#372e2d] mb-2"
								>
									Ghi chú
								</label>
								<textarea
									v-model="customerInfo.notes"
									rows="3"
									class="w-full px-4 py-2 border border-[#d8a669]/50 rounded-lg focus:ring-2 focus:ring-[#d8a669] focus:border-[#d8a669] bg-white text-[#372e2d]"
									placeholder="Yêu cầu đặc biệt (xuất hoá đơn, gửi tặng vé, nhận vé tại nhà hát...)"
								></textarea>
							</div>

							<div class="hidden lg:flex justify-between">
								<button
									type="button"
									@click="goBack"
									:disabled="isSubmitting"
									class="uppercase px-6 py-3 border-2 border-[#d8a669] rounded-lg text-[#372e2d] font-semibold hover:bg-[#fdfcf0] transition disabled:opacity-50 disabled:cursor-not-allowed"
								>
									← Quay lại
								</button>
								<button
									type="submit"
									:disabled="isSubmitting"
									class="uppercase relative px-8 py-3 bg-[#d8a669] text-white rounded-lg font-bold hover:bg-[#b8884d] hover:shadow-xl transform hover:scale-105 active:scale-95 transition-all disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none"
								>
									<span
										v-if="!isSubmitting"
										class="flex items-center gap-2"
									>
										Tiếp tục thanh toán →
									</span>
									<span
										v-else
										class="flex items-center gap-2"
									>
										<svg
											class="animate-spin h-5 w-5"
											xmlns="http://www.w3.org/2000/svg"
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
						</form>
					</div>
				</div>

				<div class="hidden lg:block lg:col-span-1">
					<div
						class="uppercase bg-[#fdfcf0] border-2 border-[#d8a669] rounded-lg shadow-lg p-6 sticky top-4"
					>
						<h3 class="text-xl font-bold mb-4 text-[#372e2d]">
							Tóm tắt đơn hàng
						</h3>

						<div class="mb-4 pb-4 border-b border-[#d8a669]/30">
							<h4 class="font-semibold mb-2 text-[#372e2d]">
								{{ showInfo.name }}
							</h4>
							<p class="text-sm text-[#372e2d]/70">
								{{ performanceInfo.date }} -
								{{ performanceInfo.time }}
							</p>
						</div>

						<div class="mb-4 pb-4 border-b border-[#d8a669]/30">
							<h4 class="font-semibold mb-2 text-[#372e2d]">
								Ghế đã chọn
							</h4>
							<div class="space-y-2">
								<div
									v-for="seat in selectedSeats"
									:key="seat.id"
									class="flex justify-between text-sm bg-white p-2 rounded-lg border border-[#d8a669]/30"
								>
									<span class="text-[#372e2d]"
										>{{ seat.full_label }} -
										{{ seat.section_name }}</span
									>
									<span
										class="font-semibold text-[#d8a669]"
										>{{ formatPrice(seat.price) }}</span
									>
								</div>
							</div>
						</div>
						<div class="mb-4 pb-4 border-b border-[#d8a669]/30">
							<label
								class="block text-sm font-medium text-[#372e2d] mb-2"
								>Mã giảm giá</label
							>
							<div class="flex gap-2">
								<input
									v-model="discountCodeInput"
									type="text"
									class="w-full px-3 py-2 border border-[#d8a669]/50 rounded-lg focus:ring-2 focus:ring-[#d8a669] bg-white text-[#372e2d]"
									placeholder="Nhập mã giảm giá"
									:disabled="
										bookingStore.isDiscountSuccess ||
										isApplyingDiscount
									"
								/>
								<button
									@click="applyDiscountCode"
									:disabled="
										bookingStore.isDiscountSuccess ||
										isApplyingDiscount
									"
									class="uppercase px-4 py-2 bg-[#d8a669] text-white rounded-lg font-semibold hover:bg-[#b8884d] disabled:bg-gray-400 disabled:cursor-not-allowed transition flex items-center gap-2 whitespace-nowrap"
								>
									<svg
										v-if="isApplyingDiscount"
										class="animate-spin h-4 w-4"
										xmlns="http://www.w3.org/2000/svg"
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
									<span>{{
										isApplyingDiscount
											? "Đang áp dụng..."
											: "Áp dụng"
									}}</span>
								</button>
							</div>
							<p
								v-if="bookingStore.discountMessage"
								class="mt-2 text-sm break-words"
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

						<div
							class="space-y-2 mb-4 pb-4 border-b border-[#d8a669]/30"
						>
							<div class="flex justify-between text-sm">
								<span class="text-[#372e2d]/70"
									>Tổng tiền vé:</span
								>
								<span class="font-semibold text-[#372e2d]">{{
									formatPrice(ticketAmount)
								}}</span>
							</div>
							<!-- <div class="flex justify-between text-sm">
								<span class="text-[#372e2d]/70"
									>Phí vận chuyển:</span
								>
								<span class="font-semibold text-[#d8a669]">
									{{ formatPrice(shippingFee) }}
								</span>
							</div> -->
							<!-- <div class="flex justify-between text-sm">
								<span class="text-[#372e2d]/70"
									>Phí dịch vụ:</span
								>
								<span class="font-semibold text-[#d8a669]">{{
									formatPrice(serviceFee)
								}}</span>
							</div> -->
							<div
								v-if="bookingStore.discountAmount > 0"
								class="flex justify-between text-sm"
							>
								<span class="text-[#372e2d]/70">Giảm giá:</span>
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
							<span class="uppercase text-[#372e2d]"
								>Tổng thanh toán:</span
							>
							<span class="text-[#d8a669] text-2xl uppercase">{{
								formatPrice(finalAmount)
							}}</span>
						</div>

						<div
							class="mt-4 p-3 bg-yellow-50 rounded-lg border border-yellow-300"
						>
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
				class="lg:hidden fixed bottom-0 left-0 right-0 bg-[#fdfcf0] border-t-2 border-[#d8a669] shadow-lg z-50"
			>
				<div class="px-4 py-3">
					<div class="flex justify-between items-center mb-3">
						<div>
							<p class="text-xs text-[#372e2d]/70">
								Tổng thanh toán
							</p>
							<p class="text-lg font-bold text-[#d8a669]">
								{{ formatPrice(finalAmount) }}
							</p>
						</div>
						<div class="text-right">
							<p class="text-xs text-[#372e2d]/70">
								⏱️ {{ formatTime(timeLeft) }}
							</p>
							<button
								@click="toggleOrderSummary"
								class="text-xs text-[#d8a669] hover:text-[#b8884d] underline font-medium"
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
						class="mb-3 p-3 bg-white rounded-lg text-sm max-h-48 overflow-y-auto border border-[#d8a669]/30"
					>
						<div class="space-y-2">
							<div class="flex justify-between">
								<span class="text-[#372e2d]/70">Tiền vé:</span>
								<span class="font-semibold text-[#372e2d]">{{
									formatPrice(ticketAmount)
								}}</span>
							</div>
							<!-- <div class="flex justify-between">
								<span class="text-[#372e2d]/70"
									>Phí dịch vụ:</span
								>
								<span class="font-semibold text-[#372e2d]">{{
									formatPrice(serviceFee)
								}}</span>
							</div> -->
							<!-- <div class="flex justify-between">
								<span class="text-[#372e2d]/70"
									>Phí vận chuyển:</span
								>
								<span class="font-semibold text-[#372e2d]">{{
									formatPrice(shippingFee)
								}}</span>
							</div> -->
							<div
								v-if="bookingStore.discountAmount > 0"
								class="flex justify-between"
							>
								<span class="text-[#372e2d]/70">Giảm giá:</span>
								<span class="font-semibold text-green-600"
									>-{{
										formatPrice(bookingStore.discountAmount)
									}}</span
								>
							</div>
							<div class="pt-2 border-t border-[#d8a669]/30">
								<label
									class="block text-xs font-medium text-[#372e2d] mb-1"
									>Mã giảm giá</label
								>
								<div class="flex gap-2">
									<input
										v-model="discountCodeInput"
										type="text"
										class="w-full px-2 py-1 text-sm border border-[#d8a669]/50 rounded-md focus:ring-1 focus:ring-[#d8a669] bg-white text-[#372e2d]"
										placeholder="Nhập mã"
										:disabled="
											bookingStore.isDiscountSuccess ||
											isApplyingDiscount
										"
									/>
									<button
										@click="applyDiscountCode"
										:disabled="
											bookingStore.isDiscountSuccess ||
											isApplyingDiscount
										"
										class="px-3 py-1 bg-[#d8a669] text-white rounded-md text-xs font-semibold hover:bg-[#b8884d] disabled:bg-gray-400 flex items-center gap-1"
									>
										<svg
											v-if="isApplyingDiscount"
											class="animate-spin h-3 w-3"
											xmlns="http://www.w3.org/2000/svg"
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
										<span>{{
											isApplyingDiscount
												? "Đang..."
												: "Áp dụng"
										}}</span>
									</button>
								</div>
								<p
									v-if="bookingStore.discountMessage"
									class="mt-1 text-xs break-words"
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
							<div class="border-t border-[#d8a669]/30 pt-2 mt-2">
								<p class="text-xs text-[#372e2d]/70 mb-1">
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
							:disabled="isSubmitting"
							class="flex-1 px-4 py-3 border-2 border-[#d8a669] rounded-lg text-[#372e2d] hover:bg-white transition font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
						>
							← Quay lại
						</button>
						<button
							@click="handleSubmit"
							:disabled="isSubmitting"
							class="flex-1 px-4 py-3 bg-[#d8a669] text-white rounded-lg font-bold hover:bg-[#b8884d] transition disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2"
						>
							<svg
								v-if="isSubmitting"
								class="animate-spin h-5 w-5"
								xmlns="http://www.w3.org/2000/svg"
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
							<span>{{
								isSubmitting ? "Đang xử lý..." : "Thanh toán →"
							}}</span>
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

// Loading states
const isSubmitting = ref(false);
const isApplyingDiscount = ref(false);

// Form data
const showInfo = ref({
	name: "",
	service_fee_per_ticket: 0,
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
	return bookingStore.shippingFee || 0;
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
		bookingStore.discountMessage = "Vui lòng nhập mã giảm giá";
		bookingStore.isDiscountSuccess = false;
		return;
	}

	isApplyingDiscount.value = true;
	try {
		await bookingStore.applyDiscount(
			discountCodeInput.value,
			customerInfo.value
		);
	} finally {
		isApplyingDiscount.value = false;
	}
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
	if (isSubmitting.value) return; // Prevent double submission

	isSubmitting.value = true;

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
			toast.error("Không có ghế được đặt. Vui lòng chọn lại.");
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
			throw new Error("Không nhận được URL thanh toán");
		}
	} catch (error) {
		console.error("Error:", error);
		bookingStore.clearBooking();
		toast.error(error.message || "Có lỗi xảy ra. Vui lòng thử lại.");

		if (error.shouldRedirect) {
			setTimeout(() => {
				router.push(`/booking/${route.params.showId}`);
			}, 1500);
		}
	} finally {
		isSubmitting.value = false;
	}
};

const goBack = () => {
	router.back();
};

const startTimer = () => {
	const savedExpiry = sessionStorage.getItem("reservationExpiry");

	if (!savedExpiry) {
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	const expiryDate = new Date(savedExpiry);
	const now = new Date();

	if (expiryDate <= now) {
		toast.error("Hết thời gian giữ ghế");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

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
};

onMounted(() => {
	bookingStore.resetDiscount();
	discountCodeInput.value = "";

	const existingSessionId = sessionStorage.getItem("session_id");
	if (existingSessionId) {
		bookingStore.sessionId = existingSessionId;
	} else {
		console.error("❌ No session ID found");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	let hasSeats = false;

	if (bookingStore.selectedSeats?.length > 0) {
		selectedSeats.value = bookingStore.selectedSeats;
		hasSeats = true;
	} else {
		const savedSeats = sessionStorage.getItem("selectedSeats");
		if (savedSeats) {
			try {
				const parsedSeats = JSON.parse(savedSeats);
				selectedSeats.value = parsedSeats;
				bookingStore.selectedSeats = parsedSeats;
				hasSeats = parsedSeats.length > 0;
			} catch (e) {
				console.error("Failed to parse savedSeats:", e);
			}
		}
	}

	if (!hasSeats) {
		console.error("❌ No seats found");
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
		showInfo.value = {
			name: bookingStore.currentShow.name,
			service_fee_per_ticket:
				bookingStore.currentShow.service_fee_per_ticket,
		};
	}

	if (!showInfo.value.name || !performanceInfo.value.date) {
		console.error("❌ Missing show or performance info");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	if (!serviceFeePerTicket.value) {
		console.error("❌ Service fee not found");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	const savedExpiry = sessionStorage.getItem("reservationExpiry");
	if (!savedExpiry) {
		console.error("❌ No reservation expiry");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	const expiryDate = new Date(savedExpiry);
	const now = new Date();
	if (expiryDate <= now) {
		console.error("❌ Reservation expired");
		toast.error("Hết thời gian giữ ghế");
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
