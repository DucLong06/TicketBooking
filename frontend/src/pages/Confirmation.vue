<template>
	<DefaultLayout>
		<div class="container mx-auto px-4 py-8">
			<!-- Success Message -->
			<div class="max-w-3xl mx-auto">
				<div class="bg-white rounded-lg shadow-lg p-8 text-center">
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

					<h1 class="text-3xl font-bold text-gray-800 mb-2">
						Đặt vé thành công!
					</h1>
					<p class="text-gray-600 mb-6">
						Cảm ơn bạn đã đặt vé. Vé điện tử đã được gửi đến email
						của bạn.
					</p>

					<!-- Booking Code -->
					<div class="bg-gray-50 rounded-lg p-6 mb-6">
						<p class="text-sm text-gray-600 mb-2">Mã đặt vé</p>
						<p class="text-2xl font-bold text-primary-600">
							{{ bookingCode }}
						</p>
					</div>

					<!-- Booking Details -->
					<div class="bg-gray-50 rounded-lg p-6 text-left mb-6">
						<h3 class="font-semibold mb-4">Chi tiết đặt vé</h3>

						<div class="space-y-3">
							<div class="flex justify-between">
								<span class="text-gray-600">Vở diễn:</span>
								<span class="font-medium">{{
									bookingData.showInfo?.name
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">Ngày diễn:</span>
								<span class="font-medium">{{
									bookingData.performance?.date
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">Suất diễn:</span>
								<span class="font-medium">{{
									bookingData.performance?.time
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">Ghế:</span>
								<span class="font-medium">{{ seatsList }}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">Người đặt:</span>
								<span class="font-medium">{{
									bookingData.customerInfo?.fullName
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">Email:</span>
								<span class="font-medium">{{
									bookingData.customerInfo?.email
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">SĐT:</span>
								<span class="font-medium">{{
									bookingData.customerInfo?.phone
								}}</span>
							</div>
							<div class="flex justify-between pt-3 border-t">
								<span class="text-gray-600 font-semibold"
									>Tổng thanh toán:</span
								>
								<span class="font-bold text-primary-600">{{
									formatPrice(bookingData.amount)
								}}</span>
							</div>
						</div>
					</div>
					<!-- 
					<div class="mb-6">
						<p class="text-sm text-gray-600 mb-3">
							Mã QR để check-in
						</p>
						<div
							class="inline-block p-4 bg-white border-2 border-gray-200 rounded-lg"
						>
							<canvas ref="qrcodeCanvas"></canvas>
						</div>
					</div> -->

					<!-- Actions -->
					<div class="flex flex-col sm:flex-row gap-4 justify-center">
						<!-- <button
							@click="downloadTicket"
							class="px-6 py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition"
						>
							<svg
								class="inline-block w-5 h-5 mr-2"
								fill="currentColor"
								viewBox="0 0 20 20"
							>
								<path
									fill-rule="evenodd"
									d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
									clip-rule="evenodd"
								></path>
							</svg>
							Tải vé
						</button> -->

						<button
							@click="sendEmail"
							:disabled="isResendingEmail"
							:class="[
								'px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold transition',
								isResendingEmail
									? 'opacity-50 cursor-not-allowed'
									: 'hover:bg-blue-700',
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
							<svg
								v-if="isResendingEmail"
								class="animate-spin -ml-1 mr-2 h-5 w-5 text-white inline-block"
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

							{{
								isResendingEmail
									? "Đang gửi..."
									: "Gửi lại email"
							}}
						</button>

						<button
							@click="goHome"
							class="px-6 py-3 border border-gray-300 rounded-lg font-semibold hover:bg-gray-50 transition"
						>
							Về trang chủ
						</button>
					</div>
				</div>

				<!-- Important Notice -->
				<div
					class="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg"
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
						<!-- <li>
							• Mã QR là duy nhất, không chia sẻ cho người khác
						</li> -->
					</ul>
				</div>
			</div>
		</div>
	</DefaultLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import QRCode from "qrcode";
import jsPDF from "jspdf";
import DefaultLayout from "../layouts/DefaultLayout.vue";
import { bookingAPI } from "../api/booking";
import { useToast } from "vue-toastification";

const toast = useToast();
const router = useRouter();
const route = useRoute();

const isResendingEmail = ref(false);
// Data
const bookingCode = ref("");
const bookingData = ref({});
const qrcodeCanvas = ref(null);

// Computed
// frontend/src/pages/Confirmation.vue

const seatsList = computed(() => {
	if (!bookingData.value?.seat_reservations) return "";
	console.log(bookingData.value.seat_reservations);

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

const generateQRCode = async () => {
	if (!qrcodeCanvas.value) return;

	const qrData = {
		bookingCode: bookingCode.value,
		amount: bookingData.value.amount,
		seats: seatsList.value,
	};

	try {
		await QRCode.toCanvas(qrcodeCanvas.value, JSON.stringify(qrData), {
			width: 200,
			margin: 2,
			color: {
				dark: "#000000",
				light: "#FFFFFF",
			},
		});
	} catch (error) {
		console.error("Failed to generate QR code:", error);
	}
};

const downloadTicket = () => {
	const pdf = new jsPDF();

	// Header
	pdf.setFontSize(20);
	pdf.text("VÉ XEM PHIM", 105, 20, { align: "center" });

	// Booking code
	pdf.setFontSize(12);
	pdf.text(`Mã đặt vé: ${bookingCode.value}`, 20, 40);

	// Show info
	pdf.text(`Vở diễn: ${bookingData.value.showInfo?.name}`, 20, 50);
	pdf.text(`Ngày: ${bookingData.value.performance?.date}`, 20, 60);
	pdf.text(`Suất: ${bookingData.value.performance?.time}`, 20, 70);
	pdf.text(`Ghế: ${seatsList.value}`, 20, 80);

	// Customer info
	pdf.text(
		`Khách hàng: ${bookingData.value.customerInfo?.fullName}`,
		20,
		100
	);
	pdf.text(`Email: ${bookingData.value.customerInfo?.email}`, 20, 110);
	pdf.text(`SĐT: ${bookingData.value.customerInfo?.phone}`, 20, 120);

	// Total
	pdf.setFontSize(14);
	pdf.text(`Tổng: ${formatPrice(bookingData.value.amount)}`, 20, 140);

	// QR Code
	if (qrcodeCanvas.value) {
		const qrImage = qrcodeCanvas.value.toDataURL("image/png");
		pdf.addImage(qrImage, "PNG", 150, 40, 40, 40);
	}

	// Footer
	pdf.setFontSize(10);
	pdf.text("Hồ Gươm Opera", 105, 280, { align: "center" });
	pdf.text("40 Hàng Bài, Hà Nội", 105, 285, { align: "center" });

	// Save
	pdf.save(`ticket-${bookingCode.value}.pdf`);
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
	// Clear all session data
	sessionStorage.clear();
	router.push("/");
};

onMounted(async () => {
	bookingCode.value = route.params.bookingCode;

	try {
		const response = await bookingAPI.getBooking(bookingCode.value);
		const rawData = response.data;

		// Transform backend data to frontend expected structure
		bookingData.value = {
			showInfo: {
				name: rawData.show_name,
			},
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
			// Keep original data for reference
			...rawData,
		};

		// Save the transformed data to sessionStorage for backup
		sessionStorage.setItem(
			"bookingData",
			JSON.stringify(bookingData.value)
		);
	} catch (error) {
		console.error("Failed to load booking data:", error);

		// Fallback to sessionStorage
		const savedData = sessionStorage.getItem("bookingData");
		if (savedData) {
			bookingData.value = JSON.parse(savedData);
		} else {
			toast.error("Không tìm thấy thông tin đặt vé");
			router.push("/");
			return;
		}
	}

	// await generateQRCode();
});
</script>
