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

					<!-- QR Code -->
					<div class="mb-6">
						<p class="text-sm text-gray-600 mb-3">
							Mã QR để check-in
						</p>
						<div
							class="inline-block p-4 bg-white border-2 border-gray-200 rounded-lg"
						>
							<canvas ref="qrcodeCanvas"></canvas>
						</div>
					</div>

					<!-- Actions -->
					<div class="flex flex-col sm:flex-row gap-4 justify-center">
						<button
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
						</button>

						<button
							@click="sendEmail"
							class="px-6 py-3 bg-gray-600 text-white rounded-lg font-semibold hover:bg-gray-700 transition"
						>
							<svg
								class="inline-block w-5 h-5 mr-2"
								fill="currentColor"
								viewBox="0 0 20 20"
							>
								<path
									d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"
								></path>
								<path
									d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"
								></path>
							</svg>
							Gửi lại email
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
						<li>
							• Mã QR là duy nhất, không chia sẻ cho người khác
						</li>
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

const router = useRouter();
const route = useRoute();

// Data
const bookingCode = ref("");
const bookingData = ref({});
const qrcodeCanvas = ref(null);

// Computed
const seatsList = computed(() => {
	if (!bookingData.value.selectedSeats) return "";
	return bookingData.value.selectedSeats
		.map((seat) => `${seat.row}${seat.number}`)
		.join(", ");
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
	alert("Email đã được gửi lại thành công!");

	// In real app, this would call API to resend email
	// await api.post('/bookings/resend-email', { bookingCode: bookingCode.value })
};

const goHome = () => {
	// Clear all session data
	sessionStorage.clear();
	router.push("/");
};

onMounted(async () => {
	// Get booking code from route
	bookingCode.value = route.params.bookingCode;

	// Load booking data from sessionStorage
	const savedData = sessionStorage.getItem("bookingData");
	if (savedData) {
		bookingData.value = JSON.parse(savedData);
	} else {
		// Mock data for testing
		bookingData.value = {
			bookingCode: bookingCode.value,
			amount: 4020000,
			showInfo: { name: "Italia Mistero" },
			performance: { date: "15/12/2024", time: "19:00" },
			selectedSeats: [
				{ row: "A", number: 5 },
				{ row: "A", number: 6 },
			],
			customerInfo: {
				fullName: "Nguyễn Văn Test",
				email: "test@example.com",
				phone: "0901234567",
			},
		};
	}

	// Generate QR code
	await generateQRCode();
});
</script>
