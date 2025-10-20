<template>
	<DefaultLayout>
		<div class="container mx-auto px-4 py-8">
			<!-- Success Message -->
			<div class="max-w-3xl mx-auto">
				<div
					class="bg-[#fdfcf0] border-2 border-[#d8a669] rounded-lg shadow-lg p-8 text-center"
				>
					<!-- Success Icon -->
					<div class="mb-6">
						<div
							class="inline-flex items-center justify-center w-20 h-20 bg-green-100 rounded-full"
						>
							<svg
								class="w-10 h-10 text-green-500"
								fill="currentColor"
								viewBox="0 0 20 20"
							>
								<path
									fill-rule="evenodd"
									d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
									clip-rule="evenodd"
								></path>
							</svg>
						</div>
					</div>

					<h1 class="text-3xl font-bold text-[#372e2d] mb-2">
						Đặt vé thành công!
					</h1>
					<p class="text-[#372e2d]/70 mb-6">
						Cảm ơn bạn đã đặt vé. Vé điện tử đã được gửi đến email
						của bạn.
					</p>

					<!-- Booking Code -->
					<div
						class="bg-white border border-[#d8a669]/30 rounded-lg p-6 mb-6"
					>
						<p class="text-sm text-[#372e2d]/70 mb-2">Mã đặt vé</p>
						<p class="text-2xl font-bold text-[#d8a669]">
							{{ bookingCode }}
						</p>
					</div>

					<!-- Booking Details -->
					<div
						class="bg-white border border-[#d8a669]/30 rounded-lg p-6 text-left mb-6"
					>
						<h3 class="font-semibold mb-4 text-[#372e2d]">
							Chi tiết đặt vé
						</h3>

						<div class="space-y-3">
							<div class="flex justify-between">
								<span class="text-[#372e2d]/70">Vở diễn:</span>
								<span class="font-medium text-[#372e2d]">{{
									bookingData.showInfo?.name
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-[#372e2d]/70"
									>Ngày diễn:</span
								>
								<span class="font-medium text-[#372e2d]">{{
									bookingData.performance?.date
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-[#372e2d]/70"
									>Suất diễn:</span
								>
								<span class="font-medium text-[#372e2d]">{{
									bookingData.performance?.time
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-[#372e2d]/70">Ghế:</span>
								<span class="font-medium text-[#372e2d]">{{
									seatsList
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-[#372e2d]/70"
									>Người đặt:</span
								>
								<span class="font-medium text-[#372e2d]">{{
									bookingData.customerInfo?.fullName
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-[#372e2d]/70">Email:</span>
								<span class="font-medium text-[#372e2d]">{{
									bookingData.customerInfo?.email
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-[#372e2d]/70">SĐT:</span>
								<span class="font-medium text-[#372e2d]">{{
									bookingData.customerInfo?.phone
								}}</span>
							</div>
							<div
								class="flex justify-between pt-3 border-t border-[#d8a669]/30"
							>
								<span class="text-[#372e2d] font-semibold"
									>Tổng thanh toán:</span
								>
								<span
									class="font-bold text-[#d8a669] text-xl"
									>{{ formatPrice(bookingData.amount) }}</span
								>
							</div>
						</div>
					</div>

					<!-- Actions -->
					<div class="flex flex-col sm:flex-row gap-4 justify-center">
						<button
							@click="sendEmail"
							:disabled="isResendingEmail"
							:class="[
								'px-6 py-3 bg-[#d8a669] text-white rounded-lg font-bold shadow-lg transition-all',
								isResendingEmail
									? 'opacity-50 cursor-not-allowed'
									: 'hover:bg-[#b8884d] hover:shadow-xl transform hover:scale-105 active:scale-95',
							]"
						>
							<svg
								v-if="!isResendingEmail"
								class="w-5 h-5 inline-block mr-2"
								fill="currentColor"
								viewBox="0 0 20 20"
							>
								<path
									fill-rule="evenodd"
									d="M2.94 6.412A2 2 0 002 8.108V16a2 2 0 002 2h12a2 2 0 002-2V8.108a2 2 0 00-.94-1.696l-6-3.75a2 2 0 00-2.12 0l-6 3.75zm3.06 2.876L8 8.382l2.94.906a2 2 0 001.12 0L15 8.382V14a1 1 0 01-1 1H6a1 1 0 01-1-1V9.288zm8-4.288V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"
								></path>
							</svg>

							<!-- Loading spinner -->
							<DuongCamLoading
								v-if="isResendingEmail"
								size="sm"
								:show-branding="false"
								:show-logo="false"
								class="inline-block -ml-1 mr-2"
							/>
							{{
								isResendingEmail
									? "Đang gửi..."
									: "Gửi lại email"
							}}
						</button>

						<button
							@click="goHome"
							class="px-6 py-3 border-2 border-[#d8a669] text-[#372e2d] rounded-lg font-semibold hover:bg-white transition"
						>
							Về trang chủ
						</button>
					</div>
				</div>

				<!-- Important Notice -->
				<div
					class="mt-6 p-4 bg-yellow-50 border-2 border-yellow-300 rounded-lg"
				>
					<h4 class="font-semibold text-yellow-800 mb-2">
						Lưu ý quan trọng:
					</h4>
					<ul class="text-sm text-yellow-700 space-y-1">
						<li>
							• Vui lòng mang theo CMND/CCCD khi đến nhận vé tại
							quầy
						</li>
						<li>
							• Quý khách vui lòng đến trước giờ diễn 30 phút để
							check-in
						</li>
						<li>• Vé đã mua không được hoàn trả hoặc đổi lịch</li>
					</ul>
				</div>
			</div>
		</div>
	</DefaultLayout>
</template>
<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import DefaultLayout from "../layouts/DefaultLayout.vue";
import { bookingAPI } from "../api/booking";
import { useToast } from "vue-toastification";
import { useBookingStore } from "../stores/booking";
const bookingStore = useBookingStore();
import DuongCamLoading from "@/components/common/DuongCamLoading.vue";

const toast = useToast();
const router = useRouter();
const route = useRoute();

const isResendingEmail = ref(false);
// Data
const bookingCode = ref("");
const bookingData = ref({});

const seatsList = computed(() => {
	if (!bookingData.value?.seat_reservations) return "";

	// Group by section
	const seatsBySection = {};
	bookingData.value.seat_reservations.forEach((seat) => {
		const sectionName = seat.section_name || "Khán phòng chính";
		if (!seatsBySection[sectionName]) {
			seatsBySection[sectionName] = [];
		}
		seatsBySection[sectionName].push(seat.seat_label);
	});

	return Object.entries(seatsBySection)
		.map(([section, seats]) => `${section}: ${seats.join(", ")}`)
		.join(" | ");
});

// Methods
const formatPrice = (price) => {
	return new Intl.NumberFormat("vi-VN", {
		style: "currency",
		currency: "VND",
	}).format(price || 0);
};

const sendEmail = async () => {
	if (isResendingEmail.value) return; // Prevent double click

	isResendingEmail.value = true;

	try {
		const response = await bookingAPI.resendEmail(bookingCode.value);

		if (response.data.success) {
			toast.success(
				response.data.message || "Email đã được gửi lại thành công!"
			);
		} else {
			toast.error(response.data.error || "Có lỗi xảy ra khi gửi email");
		}
	} catch (error) {
		console.error("Error resending email:", error);

		// Handle different error responses
		if (
			error.response &&
			error.response.data &&
			error.response.data.error
		) {
			toast.error(error.response.data.error);
		} else {
			toast.error("Không thể gửi email. Vui lòng thử lại sau.");
		}
	} finally {
		isResendingEmail.value = false;
	}
};

const goHome = () => {
	sessionStorage.clear();

	bookingStore.clearBooking();

	bookingStore.initSession();

	router.push("/");
};
function transformBookingData(rawData) {
	const required = [
		"booking_code",
		"customer_email",
		"performance_datetime",
		"seat_reservations",
	];
	for (const field of required) {
		if (!rawData[field]) {
			throw new Error(`Missing required field: ${field}`);
		}
	}

	return {
		showInfo: { name: rawData.show_name },
		performance: {
			date: new Date(rawData.performance_datetime).toLocaleDateString(
				"vi-VN"
			),
			time: new Date(rawData.performance_datetime).toLocaleTimeString(
				"vi-VN",
				{
					hour: "2-digit",
					minute: "2-digit",
				}
			),
		},
		customerInfo: {
			fullName: rawData.customer_name,
			email: rawData.customer_email,
			phone: rawData.customer_phone,
		},
		amount: rawData.final_amount,
		selectedSeats: rawData.seat_reservations.map((sr) => ({
			id: sr.seat.id,
			row: sr.seat.row,
			number: sr.seat.number,
			price: sr.price,
		})),
		...rawData,
	};
}

onMounted(async () => {
	bookingCode.value = route.params.bookingCode;

	sessionStorage.removeItem("session_id");
	sessionStorage.removeItem("selectedSeats");
	sessionStorage.removeItem("reservationExpiry");
	sessionStorage.removeItem("currentBooking");

	bookingStore.clearBooking();

	bookingStore.initSession();

	try {
		const response = await bookingAPI.getBooking(bookingCode.value);
		bookingData.value = transformBookingData(response.data);

		sessionStorage.setItem(
			"bookingData",
			JSON.stringify(bookingData.value)
		);
	} catch (error) {
		console.error("Failed to load booking:", error);

		const savedData = sessionStorage.getItem("bookingData");
		if (!savedData) {
			toast.error("Không tìm thấy thông tin đặt vé");
			router.push("/");
			return;
		}

		bookingData.value = JSON.parse(savedData);
	}
});
</script>
