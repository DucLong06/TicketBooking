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

			<!-- Main Content -->
			<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
				<!-- Form Section -->
				<div class="lg:col-span-2">
					<div
						class="bg-white rounded-lg shadow-lg p-6 mb-28 lg:mb-0"
					>
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
									@blur="fetchDiscounts"
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
									@blur="fetchDiscounts"
								/>
								<p
									v-if="errors.phone"
									class="mt-1 text-sm text-red-500"
								>
									{{ errors.phone }}
								</p>
							</div>

							<!-- Address -->
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

							<!-- Shipping Time -->
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
										Trong giờ hành chính (8h-17h)
									</option>
									<option value="after_hours">
										Ngoài giờ hành chính
									</option>
								</select>
							</div>

							<!-- Notes -->
							<div class="mb-6">
								<label
									class="block text-sm font-medium text-gray-700 mb-2"
								>
									Ghi chú (không bắt buộc)
								</label>
								<textarea
									v-model="customerInfo.notes"
									rows="2"
									class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
									placeholder="Ghi chú thêm về đơn hàng..."
								></textarea>
							</div>

							<!-- Discount Code Section -->
							<div class="mb-4 pb-4 border-b">
								<label
									class="block text-sm font-medium text-gray-700 mb-2"
								>
									Mã giảm giá
								</label>
								<div class="flex gap-2">
									<input
										v-model="discountCodeInput"
										type="text"
										class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 uppercase"
										placeholder="Nhập mã giảm giá"
										:disabled="isApplyingDiscount"
									/>
									<button
										v-if="!bookingStore.isDiscountSuccess"
										@click="applyDiscountCode"
										:disabled="
											isApplyingDiscount ||
											!discountCodeInput.trim()
										"
										type="button"
										class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition whitespace-nowrap"
									>
										{{
											isApplyingDiscount
												? "Đang xử lý..."
												: "Áp dụng"
										}}
									</button>
									<button
										v-else
										@click="removeDiscount"
										type="button"
										class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition whitespace-nowrap"
									>
										Đổi mã
									</button>
								</div>

								<!-- Available Discounts -->
								<div
									v-if="allDiscounts.length > 0"
									class="mt-3 space-y-2"
								>
									<p
										class="text-xs text-gray-600 font-medium"
									>
										Mã khuyến mãi có sẵn:
									</p>
									<div class="discount-grid">
										<button
											v-for="discount in allDiscounts"
											:key="discount.code"
											@click="
												selectDiscount(discount.code)
											"
											:disabled="
												!discount.eligible ||
												isApplyingDiscount
											"
											type="button"
											:class="[
												'discount-btn px-3 py-2 rounded-lg text-xs font-semibold transition border',
												discount.eligible
													? 'bg-gradient-to-r from-orange-50 to-red-50 border-orange-300 text-orange-700 hover:from-orange-100 hover:to-red-100 cursor-pointer'
													: 'bg-gray-100 border-gray-300 text-gray-400 cursor-not-allowed opacity-60',
											]"
											:title="
												discount.eligible
													? discount.description
													: discount.reason
											"
										>
											<span class="block font-bold">{{
												discount.code
											}}</span>
											<span
												v-if="
													discount.min_ticket_quantity
												"
												class="block text-[10px] mt-1"
											>
												{{
													discount.eligible
														? `✓ ${discount.min_ticket_quantity}+ vé`
														: `Cần ${discount.min_ticket_quantity}+ vé`
												}}
											</span>
											<span
												v-if="discount.value"
												class="block text-[10px] mt-0.5"
											>
												{{
													discount.discount_type ===
													"PERCENTAGE"
														? `Giảm ${discount.value}%`
														: `Giảm ${formatPrice(
																discount.value
														  )}`
												}}
											</span>
										</button>
									</div>
									<p
										v-if="unavailableDiscountsCount > 0"
										class="text-[10px] text-gray-500 italic mt-2"
									>
										💡 Mua thêm vé để mở khóa
										{{ unavailableDiscountsCount }} mã giảm
										giá
									</p>
								</div>

								<!-- Discount Message -->
								<p
									v-if="bookingStore.discountMessage"
									class="mt-2 text-sm font-medium"
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

							<!-- Desktop Buttons -->
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
									:disabled="isSubmitting"
									class="px-8 py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 disabled:bg-gray-400 transition"
								>
									{{
										isSubmitting
											? "Đang xử lý..."
											: "Tiếp tục thanh toán →"
									}}
								</button>
							</div>
						</form>
					</div>
				</div>

				<!-- Order Summary - Desktop -->
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
								<span class="text-gray-600">Tiền vé:</span>
								<span class="font-semibold">{{
									formatPrice(ticketAmount)
								}}</span>
							</div>
							<div class="flex justify-between text-sm">
								<span class="text-gray-600"
									>Phí vận chuyển:</span
								>
								<span class="font-semibold">{{
									formatPrice(serviceFee)
								}}</span>
							</div>
							<div
								v-if="bookingStore.discountAmount > 0"
								class="flex justify-between text-sm"
							>
								<span class="text-gray-600">Giảm giá:</span>
								<span class="font-semibold text-green-600">
									-{{
										formatPrice(bookingStore.discountAmount)
									}}
								</span>
							</div>
						</div>

						<!-- Total -->
						<div class="flex justify-between text-lg font-bold">
							<span>Tổng cộng:</span>
							<span class="text-primary-600">{{
								formatPrice(finalAmount)
							}}</span>
						</div>

						<!-- Timer -->
						<div
							class="mt-4 p-3 bg-orange-50 rounded-lg text-center"
						>
							<p class="text-sm text-gray-600 mb-1">
								Thời gian giữ ghế còn lại:
							</p>
							<p class="text-2xl font-bold text-orange-600">
								{{ formatTime(timeLeft) }}
							</p>
						</div>
					</div>
				</div>
			</div>

			<!-- Mobile Fixed Bottom Bar -->
			<div
				class="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg z-50"
			>
				<div class="container mx-auto px-4 py-3">
					<!-- Order Summary Toggle -->
					<div class="mb-3">
						<div class="flex items-center justify-between">
							<div>
								<p class="text-sm text-gray-600">Tổng cộng:</p>
								<p class="text-lg font-bold text-primary-600">
									{{ formatPrice(finalAmount) }}
								</p>
							</div>
							<button
								type="button"
								@click="toggleOrderSummary"
								class="text-sm text-primary-600 font-medium"
							>
								{{
									showOrderSummary
										? "Ẩn chi tiết"
										: "Xem chi tiết"
								}}
							</button>
						</div>
					</div>

					<!-- Collapsible Details -->
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
							<div
								v-if="bookingStore.discountAmount > 0"
								class="flex justify-between"
							>
								<span class="text-gray-600">Giảm giá:</span>
								<span class="font-semibold text-green-600">
									-{{
										formatPrice(bookingStore.discountAmount)
									}}
								</span>
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

					<!-- Action Buttons -->
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
							:disabled="isSubmitting"
							class="flex-1 px-4 py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 disabled:bg-gray-400 transition"
						>
							{{
								isSubmitting ? "Đang xử lý..." : "Thanh toán →"
							}}
						</button>
					</div>
				</div>
			</div>
		</div>
	</DefaultLayout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from "vue";
import { useRouter, useRoute } from "vue-router";
import DefaultLayout from "../layouts/DefaultLayout.vue";
import { useBookingStore } from "../stores/booking";
import { bookingAPI } from "../api/booking";
import { useToast } from "vue-toastification";

const toast = useToast();
const bookingStore = useBookingStore();
const router = useRouter();
const route = useRoute();

// State
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
	address: "",
	notes: "",
	shippingTime: "business_hours",
});

const errors = ref({});
const selectedSeats = ref([]);
const timeLeft = ref(600);
const showOrderSummary = ref(false);
const isSubmitting = ref(false);
const isApplyingDiscount = ref(false);

// Discount
const discountCodeInput = ref("");
const allDiscounts = ref([]);

// Descriptions
const addressDescription = ref(
	"Địa chỉ nhận vé cứng. Nhà hát Hồ Gươm chỉ sử dụng vé cứng để vào cửa."
);
const emailDescription = ref(
	"Email để nhận xác nhận thanh toán hoặc xác nhận đặt vé"
);

let timer = null;
let toastId = null;

// Computed
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
	return ticketAmount.value + serviceFee.value;
});

const finalAmount = computed(() => {
	if (bookingStore.currentBooking?.final_amount) {
		return bookingStore.currentBooking.final_amount;
	}
	return totalAmount.value - (bookingStore.discountAmount || 0);
});

const unavailableDiscountsCount = computed(
	() => allDiscounts.value.filter((d) => !d.eligible).length
);

// Methods
const formatPrice = (price) => {
	return new Intl.NumberFormat("vi-VN", {
		style: "currency",
		currency: "VND",
	}).format(price || 0);
};

const formatTime = (seconds) => {
	const mins = Math.floor(seconds / 60);
	const secs = seconds % 60;
	return `${mins}:${secs.toString().padStart(2, "0")}`;
};

const toggleOrderSummary = () => {
	showOrderSummary.value = !showOrderSummary.value;
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

const fetchDiscounts = async () => {
	if (selectedSeats.value.length === 0) return;

	try {
		const response = await bookingAPI.getAvailableDiscounts(
			selectedSeats.value.length,
			customerInfo.value.email,
			customerInfo.value.phone
		);

		const eligibleDiscounts = response.data.discounts.map((d) => ({
			...d,
			eligible: true,
		}));

		const allResponse = await bookingAPI.getAvailableDiscounts(
			999,
			customerInfo.value.email,
			customerInfo.value.phone,
			true
		);

		const unavailableFromAPI = allResponse.data.unavailable_discounts || [];

		const ineligibleDiscounts = unavailableFromAPI
			.filter((d) => !eligibleDiscounts.some((ed) => ed.code === d.code))
			.map((d) => ({
				...d,
				eligible: false,
				reason:
					d.reason ||
					`Cần mua tối thiểu ${d.min_ticket_quantity} vé (đang có ${selectedSeats.value.length})`,
			}));

		allDiscounts.value = [...eligibleDiscounts, ...ineligibleDiscounts];

		console.log("✅ Loaded discounts:", {
			eligible: eligibleDiscounts.length,
			ineligible: ineligibleDiscounts.length,
			total: allDiscounts.value.length,
		});
	} catch (error) {
		console.error("Failed to fetch discounts:", error);
	}
};
const applyDiscountCode = async () => {
	if (!discountCodeInput.value.trim()) {
		if (toastId) toast.dismiss(toastId);
		toastId = toast.warning("Vui lòng nhập mã giảm giá.");
		return;
	}

	if (isApplyingDiscount.value) return;

	isApplyingDiscount.value = true;

	try {
		await bookingStore.applyDiscount(
			discountCodeInput.value.trim(),
			customerInfo.value
		);
	} catch (error) {
		console.error("Error applying discount:", error);
	} finally {
		isApplyingDiscount.value = false;
	}
};

const removeDiscount = () => {
	bookingStore.isDiscountSuccess = false;
	bookingStore.discountMessage = "";
	bookingStore.customerInfo.discount_code = "";
	discountCodeInput.value = "";

	if (bookingStore.currentBooking) {
		bookingStore.currentBooking.discount_amount = 0;
		bookingStore.currentBooking.final_amount =
			bookingStore.currentBooking.total_amount +
			bookingStore.currentBooking.service_fee;
	}

	toast.info("Đã xóa mã giảm giá. Vui lòng nhập mã mới.");
};

const selectDiscount = async (code) => {
	if (isApplyingDiscount.value) return;

	if (bookingStore.isDiscountSuccess) {
		removeDiscount();
		await nextTick();
	}
	discountCodeInput.value = code;
	applyDiscountCode();
};

const handleSubmit = async () => {
	if (!validateForm()) return;

	if (isSubmitting.value) return;

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
		toast.error("Không tìm thấy thông tin đặt vé. Vui lòng chọn lại.");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	const expiryDate = new Date(savedExpiry);
	const now = new Date();

	if (expiryDate <= now) {
		toast.error("Hết thời gian giữ ghế. Vui lòng đặt lại.");
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

// Lifecycle
onMounted(() => {
	// Load data from store/session
	const savedSeats = sessionStorage.getItem("selectedSeats");
	if (!savedSeats) {
		toast.error("Không tìm thấy ghế đã chọn. Vui lòng chọn lại.");
		router.push(`/booking/${route.params.showId}/seats`);
		return;
	}

	selectedSeats.value = JSON.parse(savedSeats);

	const savedShow = sessionStorage.getItem("currentShow");
	if (savedShow) {
		showInfo.value = JSON.parse(savedShow);
	}

	const savedPerformance = sessionStorage.getItem("selectedPerformance");
	if (savedPerformance) {
		performanceInfo.value = JSON.parse(savedPerformance);
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
	startTimer();

	// Fetch available discounts
	fetchDiscounts();
});

onUnmounted(() => {
	if (timer) {
		clearInterval(timer);
	}
	discountCodeInput.value = "";
});

// Watch seat changes to refetch discounts
watch(
	() => selectedSeats.value.length,
	() => {
		fetchDiscounts();
	}
);
</script>

<style scoped>
/* Discount Grid */
.discount-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
	gap: 0.5rem;
}

@media (max-width: 640px) {
	.discount-grid {
		grid-template-columns: repeat(2, 1fr);
		max-height: 200px;
		overflow-y: auto;
		padding: 0.5rem;
		border: 1px solid #e5e7eb;
		border-radius: 0.5rem;
	}
}

/* Discount Button */
.discount-btn {
	min-height: 56px;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	text-align: center;
}

@media (min-width: 768px) {
	.discount-btn {
		min-height: 64px;
	}
}

/* Touch-friendly on mobile */
@media (max-width: 640px) {
	.discount-btn {
		min-height: 60px;
		padding: 0.75rem;
	}
}

/* Smooth transitions */
.discount-btn:not(:disabled):hover {
	transform: translateY(-1px);
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.discount-btn:not(:disabled):active {
	transform: translateY(0);
}

/* Disabled state */
.discount-btn:disabled {
	pointer-events: none;
}

/* Scrollbar styling for discount grid on mobile */
@media (max-width: 640px) {
	.discount-grid::-webkit-scrollbar {
		width: 4px;
	}

	.discount-grid::-webkit-scrollbar-track {
		background: #f1f1f1;
		border-radius: 4px;
	}

	.discount-grid::-webkit-scrollbar-thumb {
		background: #d1d5db;
		border-radius: 4px;
	}

	.discount-grid::-webkit-scrollbar-thumb:hover {
		background: #9ca3af;
	}
}

/* Animation for messages */
@keyframes slideIn {
	from {
		opacity: 0;
		transform: translateY(-10px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}

.discount-btn,
p[class*="text-green-600"],
p[class*="text-red-500"] {
	animation: slideIn 0.3s ease-out;
}

/* Loading state for apply button */
button:disabled {
	cursor: not-allowed;
	opacity: 0.6;
}

/* Mobile bottom bar shadow */
@media (max-width: 1024px) {
	.fixed.bottom-0 {
		box-shadow: 0 -4px 6px -1px rgba(0, 0, 0, 0.1),
			0 -2px 4px -1px rgba(0, 0, 0, 0.06);
	}
}

/* Collapsible content animation */
.order-summary-enter-active,
.order-summary-leave-active {
	transition: all 0.3s ease;
	max-height: 200px;
	overflow: hidden;
}

.order-summary-enter-from,
.order-summary-leave-to {
	max-height: 0;
	opacity: 0;
}
</style>
