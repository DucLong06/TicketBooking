<template>
	<div class="payment-success-container">
		<div class="success-card">
			<!-- Confetti Animation -->
			<div class="confetti" v-if="showConfetti">
				<span v-for="i in 50" :key="i" class="confetti-piece"></span>
			</div>

			<!-- Success Animation -->
			<div class="success-animation">
				<transition name="scale" appear>
					<div class="checkmark-circle">
						<svg class="checkmark" viewBox="0 0 52 52">
							<circle
								class="checkmark-circle-bg"
								cx="26"
								cy="26"
								r="25"
								fill="none"
							/>
							<path
								class="checkmark-check"
								fill="none"
								d="M14.1 27.2l7.1 7.2 16.7-16.8"
							/>
						</svg>
					</div>
				</transition>
			</div>

			<!-- Success Message -->
			<transition name="fade" appear>
				<div class="message-section">
					<h1 class="title">Thanh Toán Thành Công!</h1>
					<p class="subtitle">
						Chúc mừng! Giao dịch của bạn đã được xử lý thành công.
					</p>
				</div>
			</transition>

			<!-- Booking Details Card -->
			<transition name="slide-up" appear>
				<div class="booking-card" v-if="bookingDetails">
					<div class="booking-header">
						<Film class="booking-icon" />
						<h3 class="booking-title">Thông Tin Đặt Vé</h3>
					</div>

					<div class="booking-content">
						<div class="info-row">
							<MapPin class="info-icon" />
							<div class="info-details">
								<span class="info-label">Rạp chiếu</span>
								<span class="info-value">{{
									bookingDetails.cinema
								}}</span>
							</div>
						</div>

						<div class="info-row">
							<Calendar class="info-icon" />
							<div class="info-details">
								<span class="info-label">Ngày chiếu</span>
								<span class="info-value">{{
									formatDate(bookingDetails.showDate)
								}}</span>
							</div>
						</div>

						<div class="info-row">
							<Clock class="info-icon" />
							<div class="info-details">
								<span class="info-label">Suất chiếu</span>
								<span class="info-value">{{
									bookingDetails.showTime
								}}</span>
							</div>
						</div>

						<div class="info-row">
							<Users class="info-icon" />
							<div class="info-details">
								<span class="info-label">Ghế đã đặt</span>
								<span class="info-value">{{
									bookingDetails.seats.join(", ")
								}}</span>
							</div>
						</div>

						<div class="info-row">
							<Popcorn class="info-icon" />
							<div
								class="info-details"
								v-if="
									bookingDetails.concessions &&
									bookingDetails.concessions.length
								"
							>
								<span class="info-label">Bắp nước</span>
								<span class="info-value">
									<div
										v-for="item in bookingDetails.concessions"
										:key="item.id"
									>
										{{ item.name }} x{{ item.quantity }}
									</div>
								</span>
							</div>
						</div>
					</div>
				</div>
			</transition>

			<!-- Transaction Summary -->
			<transition name="slide-up" appear>
				<div class="transaction-summary">
					<div class="summary-row">
						<span class="summary-label">Mã đặt vé:</span>
						<span class="summary-value booking-code">{{
							transactionDetails.bookingCode
						}}</span>
					</div>
					<div class="summary-row">
						<span class="summary-label">Mã giao dịch:</span>
						<span class="summary-value">{{
							transactionDetails.transactionId
						}}</span>
					</div>
					<div class="summary-row">
						<span class="summary-label">Phương thức:</span>
						<span class="summary-value">
							<CreditCard class="payment-method-icon" />
							{{ transactionDetails.paymentMethod }}
						</span>
					</div>
					<div class="summary-row total">
						<span class="summary-label">Tổng thanh toán:</span>
						<span class="summary-value">{{
							formatCurrency(transactionDetails.amount)
						}}</span>
					</div>
				</div>
			</transition>

			<!-- QR Code Section -->
			<transition name="fade" appear>
				<div class="qr-section" v-if="qrCodeUrl">
					<div class="qr-card">
						<img :src="qrCodeUrl" alt="QR Code" class="qr-code" />
						<p class="qr-text">Quét mã QR để lấy vé tại quầy</p>
					</div>
				</div>
			</transition>

			<!-- Action Buttons -->
			<transition name="slide-up" appear>
				<div class="action-buttons">
					<button @click="downloadTicket" class="btn btn-primary">
						<Download class="btn-icon" />
						Tải Vé
					</button>
					<button @click="sendEmail" class="btn btn-secondary">
						<Mail class="btn-icon" />
						Gửi Email
					</button>
					<button @click="viewBookingDetails" class="btn btn-outline">
						<Eye class="btn-icon" />
						Xem Chi Tiết
					</button>
				</div>
			</transition>

			<!-- Additional Options -->
			<transition name="fade" appear>
				<div class="additional-options">
					<button @click="bookAnother" class="option-link">
						<Plus class="option-icon" />
						Đặt vé khác
					</button>
					<button @click="goToHome" class="option-link">
						<Home class="option-icon" />
						Về trang chủ
					</button>
				</div>
			</transition>

			<!-- Notification -->
			<transition name="slide-up">
				<div class="notification" v-if="showNotification">
					<CheckCircle class="notification-icon" />
					<p class="notification-text">{{ notificationMessage }}</p>
				</div>
			</transition>
		</div>

		<!-- Background Elements -->
		<div class="bg-elements">
			<div class="bg-circle bg-circle-1"></div>
			<div class="bg-circle bg-circle-2"></div>
			<div class="bg-circle bg-circle-3"></div>
		</div>
	</div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
	CheckCircle,
	Film,
	MapPin,
	Calendar,
	Clock,
	Users,
	CreditCard,
	Download,
	Mail,
	Eye,
	Plus,
	Home,
	Popcorn,
} from "lucide-vue-next";
import QRCode from "qrcode";
import axios from "axios";

export default {
	name: "PaymentSuccess",
	components: {
		CheckCircle,
		Film,
		MapPin,
		Calendar,
		Clock,
		Users,
		CreditCard,
		Download,
		Mail,
		Eye,
		Plus,
		Home,
		Popcorn,
	},
	setup() {
		const route = useRoute();
		const router = useRouter();

		const showConfetti = ref(false);
		const showNotification = ref(false);
		const notificationMessage = ref("");
		const qrCodeUrl = ref("");

		const transactionDetails = ref({
			bookingCode: "",
			transactionId: "",
			paymentMethod: "VNPAY",
			amount: 0,
			timestamp: new Date(),
		});

		const bookingDetails = ref(null);

		const formatCurrency = (amount) => {
			return new Intl.NumberFormat("vi-VN", {
				style: "currency",
				currency: "VND",
			}).format(amount);
		};

		const formatDate = (date) => {
			return new Date(date).toLocaleDateString("vi-VN", {
				weekday: "long",
				year: "numeric",
				month: "long",
				day: "numeric",
			});
		};

		const generateQRCode = async (bookingCode) => {
			try {
				const url = await QRCode.toDataURL(bookingCode, {
					width: 200,
					margin: 2,
					color: {
						dark: "#1f2937",
						light: "#ffffff",
					},
				});
				qrCodeUrl.value = url;
			} catch (error) {
				console.error("Error generating QR code:", error);
			}
		};

		const fetchBookingDetails = async (bookingCode) => {
			try {
				const response = await axios.get(
					`/api/bookings/${bookingCode}`
				);
				bookingDetails.value = response.data;
			} catch (error) {
				console.error("Error fetching booking details:", error);
				// Use mock data for demonstration
				bookingDetails.value = {
					cinema: "CGV Vincom Center",
					showDate: new Date(),
					showTime: "19:30",
					seats: ["H8", "H9"],
					movie: "Avatar: The Way of Water",
					concessions: [{ id: 1, name: "Combo Couple", quantity: 1 }],
				};
			}
		};

		const downloadTicket = async () => {
			try {
				// Call API to download ticket PDF
				const response = await axios.get(
					`/api/bookings/${transactionDetails.value.bookingCode}/download`,
					{ responseType: "blob" }
				);

				const url = window.URL.createObjectURL(
					new Blob([response.data])
				);
				const link = document.createElement("a");
				link.href = url;
				link.setAttribute(
					"download",
					`ticket-${transactionDetails.value.bookingCode}.pdf`
				);
				document.body.appendChild(link);
				link.click();
				link.remove();

				showNotificationMessage("Vé đã được tải xuống!");
			} catch (error) {
				console.error("Error downloading ticket:", error);
				showNotificationMessage("Không thể tải vé. Vui lòng thử lại.");
			}
		};

		const sendEmail = async () => {
			try {
				await axios.post(
					`/api/bookings/${transactionDetails.value.bookingCode}/send-email`
				);
				showNotificationMessage("Email đã được gửi thành công!");
			} catch (error) {
				console.error("Error sending email:", error);
				showNotificationMessage(
					"Không thể gửi email. Vui lòng thử lại."
				);
			}
		};

		const viewBookingDetails = () => {
			router.push(
				`/booking/confirmation/${transactionDetails.value.bookingCode}`
			);
		};

		const bookAnother = () => {
			router.push("/movies");
		};

		const goToHome = () => {
			router.push("/");
		};

		const showNotificationMessage = (message) => {
			notificationMessage.value = message;
			showNotification.value = true;
			setTimeout(() => {
				showNotification.value = false;
			}, 3000);
		};

		onMounted(async () => {
			// Show confetti animation
			showConfetti.value = true;
			setTimeout(() => {
				showConfetti.value = false;
			}, 5000);

			// Get booking code from route
			const bookingCode =
				route.params.bookingCode || route.query.bookingCode;

			if (bookingCode) {
				transactionDetails.value.bookingCode = bookingCode;

				// Generate QR code
				await generateQRCode(bookingCode);

				// Fetch booking details
				await fetchBookingDetails(bookingCode);
			}

			// Get transaction details from sessionStorage
			const storedTransaction = sessionStorage.getItem("lastTransaction");
			if (storedTransaction) {
				const parsed = JSON.parse(storedTransaction);
				transactionDetails.value = {
					...transactionDetails.value,
					...parsed,
				};
			}

			// Clear the stored transaction
			sessionStorage.removeItem("lastTransaction");
		});

		return {
			showConfetti,
			showNotification,
			notificationMessage,
			qrCodeUrl,
			transactionDetails,
			bookingDetails,
			formatCurrency,
			formatDate,
			downloadTicket,
			sendEmail,
			viewBookingDetails,
			bookAnother,
			goToHome,
		};
	},
};
</script>

<style scoped>
.payment-success-container {
	min-height: 100vh;
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 20px;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	position: relative;
	overflow: hidden;
}

.success-card {
	background: white;
	border-radius: 24px;
	padding: 48px;
	max-width: 700px;
	width: 100%;
	box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
	position: relative;
	z-index: 10;
}

/* Confetti Animation */
.confetti {
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	overflow: hidden;
	z-index: 100;
	pointer-events: none;
}

.confetti-piece {
	position: absolute;
	width: 10px;
	height: 10px;
	background: linear-gradient(to right, #667eea, #764ba2, #f472b6, #fbbf24);
	animation: confetti-fall 3s ease-out forwards;
}

.confetti-piece:nth-child(odd) {
	width: 8px;
	height: 8px;
	animation-duration: 2.5s;
	background: linear-gradient(to right, #f472b6, #fbbf24);
}

.confetti-piece:nth-child(even) {
	border-radius: 50%;
}

.confetti-piece:nth-child(3n) {
	animation-delay: 0.2s;
}

.confetti-piece:nth-child(4n) {
	animation-delay: 0.4s;
	width: 6px;
	height: 6px;
}

.confetti-piece:nth-child(5n) {
	animation-delay: 0.6s;
}

@keyframes confetti-fall {
	0% {
		top: -10%;
		transform: translateX(0) rotateZ(0deg);
		opacity: 1;
	}
	100% {
		top: 100%;
		transform: translateX(calc(var(--random-x, 100) * 1px)) rotateZ(720deg);
		opacity: 0;
	}
}

/* Set random X positions */
.confetti-piece:nth-child(1) {
	left: 10%;
	--random-x: -50;
}
.confetti-piece:nth-child(2) {
	left: 20%;
	--random-x: 80;
}
.confetti-piece:nth-child(3) {
	left: 30%;
	--random-x: -30;
}
.confetti-piece:nth-child(4) {
	left: 40%;
	--random-x: 60;
}
.confetti-piece:nth-child(5) {
	left: 50%;
	--random-x: -70;
}
.confetti-piece:nth-child(6) {
	left: 60%;
	--random-x: 40;
}
.confetti-piece:nth-child(7) {
	left: 70%;
	--random-x: -20;
}
.confetti-piece:nth-child(8) {
	left: 80%;
	--random-x: 90;
}
.confetti-piece:nth-child(9) {
	left: 90%;
	--random-x: -60;
}
.confetti-piece:nth-child(10) {
	left: 15%;
	--random-x: 50;
}

/* Success Animation */
.success-animation {
	display: flex;
	justify-content: center;
	margin-bottom: 32px;
}

.checkmark-circle {
	width: 100px;
	height: 100px;
	position: relative;
}

.checkmark {
	width: 100px;
	height: 100px;
}

.checkmark-circle-bg {
	stroke: #10b981;
	stroke-width: 2;
	stroke-dasharray: 166;
	stroke-dashoffset: 166;
	animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}

.checkmark-check {
	stroke: #10b981;
	stroke-width: 3;
	stroke-linecap: round;
	stroke-dasharray: 48;
	stroke-dashoffset: 48;
	animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.6s forwards;
}

@keyframes stroke {
	100% {
		stroke-dashoffset: 0;
	}
}

/* Message Section */
.message-section {
	text-align: center;
	margin-bottom: 40px;
}

.title {
	font-size: 32px;
	font-weight: 700;
	color: #1f2937;
	margin-bottom: 12px;
	background: linear-gradient(135deg, #667eea, #764ba2);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
}

.subtitle {
	font-size: 18px;
	color: #6b7280;
	line-height: 1.6;
}

/* Booking Details Card */
.booking-card {
	background: linear-gradient(135deg, #f3f4f6, #fafafa);
	border-radius: 16px;
	padding: 24px;
	margin-bottom: 32px;
}

.booking-header {
	display: flex;
	align-items: center;
	gap: 12px;
	margin-bottom: 24px;
	padding-bottom: 16px;
	border-bottom: 2px solid #e5e7eb;
}

.booking-icon {
	width: 24px;
	height: 24px;
	color: #667eea;
}

.booking-title {
	font-size: 20px;
	font-weight: 600;
	color: #1f2937;
}

.booking-content {
	display: grid;
	gap: 20px;
}

.info-row {
	display: flex;
	align-items: flex-start;
	gap: 12px;
}

.info-icon {
	width: 20px;
	height: 20px;
	color: #9ca3af;
	flex-shrink: 0;
	margin-top: 2px;
}

.info-details {
	flex: 1;
	display: flex;
	flex-direction: column;
	gap: 4px;
}

.info-label {
	font-size: 14px;
	color: #6b7280;
}

.info-value {
	font-size: 16px;
	font-weight: 600;
	color: #1f2937;
}

/* Transaction Summary */
.transaction-summary {
	background: #f9fafb;
	border-radius: 12px;
	padding: 20px;
	margin-bottom: 32px;
}

.summary-row {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 12px 0;
	border-bottom: 1px solid #e5e7eb;
}

.summary-row:last-child {
	border-bottom: none;
}

.summary-row.total {
	margin-top: 8px;
	padding-top: 20px;
	border-top: 2px solid #e5e7eb;
	border-bottom: none;
}

.summary-label {
	font-size: 15px;
	color: #6b7280;
}

.summary-value {
	font-size: 15px;
	font-weight: 600;
	color: #1f2937;
	display: flex;
	align-items: center;
	gap: 8px;
}

.booking-code {
	font-family: "Courier New", monospace;
	background: linear-gradient(135deg, #667eea, #764ba2);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
	font-size: 18px;
}

.payment-method-icon {
	width: 16px;
	height: 16px;
}

.summary-row.total .summary-value {
	font-size: 20px;
	color: #10b981;
}

/* QR Code Section */
.qr-section {
	display: flex;
	justify-content: center;
	margin-bottom: 32px;
}

.qr-card {
	text-align: center;
	padding: 20px;
	background: white;
	border: 2px solid #e5e7eb;
	border-radius: 12px;
}

.qr-code {
	width: 150px;
	height: 150px;
	margin-bottom: 12px;
}

.qr-text {
	font-size: 14px;
	color: #6b7280;
}

/* Action Buttons */
.action-buttons {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
	gap: 12px;
	margin-bottom: 24px;
}

.btn {
	padding: 14px 20px;
	border-radius: 12px;
	font-size: 15px;
	font-weight: 600;
	border: none;
	cursor: pointer;
	transition: all 0.3s ease;
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
}

.btn-icon {
	width: 18px;
	height: 18px;
}

.btn-primary {
	background: linear-gradient(135deg, #667eea, #764ba2);
	color: white;
}

.btn-primary:hover {
	transform: translateY(-2px);
	box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
	background: #f3f4f6;
	color: #4b5563;
}

.btn-secondary:hover {
	background: #e5e7eb;
}

.btn-outline {
	background: transparent;
	color: #667eea;
	border: 2px solid #667eea;
}

.btn-outline:hover {
	background: #667eea;
	color: white;
}

/* Additional Options */
.additional-options {
	display: flex;
	justify-content: center;
	gap: 24px;
	padding-top: 20px;
	border-top: 1px solid #e5e7eb;
}

.option-link {
	display: flex;
	align-items: center;
	gap: 6px;
	font-size: 14px;
	color: #6b7280;
	text-decoration: none;
	background: none;
	border: none;
	cursor: pointer;
	transition: color 0.3s ease;
}

.option-link:hover {
	color: #667eea;
}

.option-icon {
	width: 16px;
	height: 16px;
}

/* Notification */
.notification {
	position: fixed;
	bottom: 30px;
	left: 50%;
	transform: translateX(-50%);
	background: white;
	padding: 16px 24px;
	border-radius: 12px;
	box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
	display: flex;
	align-items: center;
	gap: 12px;
	z-index: 1000;
}

.notification-icon {
	width: 20px;
	height: 20px;
	color: #10b981;
}

.notification-text {
	font-size: 15px;
	font-weight: 500;
	color: #1f2937;
}

/* Background Elements */
.bg-elements {
	position: absolute;
	width: 100%;
	height: 100%;
	top: 0;
	left: 0;
	z-index: 1;
	overflow: hidden;
}

.bg-circle {
	position: absolute;
	border-radius: 50%;
	background: rgba(255, 255, 255, 0.1);
	animation: float 20s infinite;
}

.bg-circle-1 {
	width: 400px;
	height: 400px;
	top: -200px;
	right: -200px;
}

.bg-circle-2 {
	width: 300px;
	height: 300px;
	bottom: -150px;
	left: -150px;
	animation-delay: 7s;
}

.bg-circle-3 {
	width: 200px;
	height: 200px;
	top: 50%;
	left: 50%;
	animation-delay: 14s;
}

@keyframes float {
	0%,
	100% {
		transform: translate(0, 0) scale(1);
	}
	33% {
		transform: translate(30px, -30px) scale(1.1);
	}
	66% {
		transform: translate(-20px, 20px) scale(0.9);
	}
}

/* Transitions */
.scale-enter-active {
	animation: scale-in 0.6s ease-out;
}

@keyframes scale-in {
	0% {
		transform: scale(0);
		opacity: 0;
	}
	50% {
		transform: scale(1.1);
	}
	100% {
		transform: scale(1);
		opacity: 1;
	}
}

.fade-enter-active {
	transition: opacity 0.5s ease;
}

.fade-enter-from {
	opacity: 0;
}

.slide-up-enter-active {
	transition: all 0.5s ease;
}

.slide-up-enter-from {
	transform: translateY(30px);
	opacity: 0;
}

/* Responsive */
@media (max-width: 640px) {
	.success-card {
		padding: 24px;
	}

	.title {
		font-size: 24px;
	}

	.subtitle {
		font-size: 16px;
	}

	.action-buttons {
		grid-template-columns: 1fr;
	}

	.additional-options {
		flex-direction: column;
		gap: 12px;
	}

	.booking-card {
		padding: 16px;
	}

	.checkmark-circle {
		width: 80px;
		height: 80px;
	}

	.checkmark {
		width: 80px;
		height: 80px;
	}
}
</style>
