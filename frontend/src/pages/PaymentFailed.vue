<template>
	<div class="payment-result-container">
		<div class="payment-card" :class="`severity-${responseInfo.severity}`">
			<!-- Animated Icon -->
			<div class="icon-wrapper">
				<transition name="bounce" appear>
					<div
						class="icon-circle"
						:style="{ backgroundColor: responseInfo.color + '20' }"
					>
						<component
							:is="iconComponent"
							class="main-icon"
							:style="{ color: responseInfo.color }"
						/>
					</div>
				</transition>
			</div>

			<!-- Error Code Badge -->
			<div
				class="error-code-badge"
				:style="{ backgroundColor: responseInfo.color }"
			>
				MÃ LỖI: {{ errorCode }}
			</div>

			<!-- Main Message -->
			<transition name="fade" appear>
				<div class="message-section">
					<h1 class="title">Thanh Toán Thất Bại</h1>
					<p class="error-message">{{ responseInfo.message }}</p>
				</div>
			</transition>

			<!-- Additional Info -->
			<transition name="slide-up" appear>
				<div
					class="info-section"
					v-if="responseInfo.additionalInfo || responseInfo.action"
				>
					<div class="info-card">
						<AlertCircle class="info-icon" />
						<div class="info-text">
							<p v-if="responseInfo.additionalInfo">
								{{ responseInfo.additionalInfo }}
							</p>
							<p v-if="responseInfo.action" class="action-text">
								{{ responseInfo.action }}
							</p>
						</div>
					</div>
				</div>
			</transition>

			<!-- Transaction Details -->
			<transition name="slide-up" appear>
				<div class="details-section" v-if="transactionDetails">
					<h3 class="details-title">Chi tiết giao dịch</h3>
					<div class="details-grid">
						<div class="detail-item">
							<span class="detail-label">Mã giao dịch:</span>
							<span class="detail-value">{{
								transactionDetails.transactionId
							}}</span>
						</div>
						<div class="detail-item">
							<span class="detail-label">Số tiền:</span>
							<span class="detail-value">{{
								formatCurrency(transactionDetails.amount)
							}}</span>
						</div>
						<div class="detail-item">
							<span class="detail-label">Thời gian:</span>
							<span class="detail-value">{{
								formatDateTime(transactionDetails.timestamp)
							}}</span>
						</div>
						<div
							class="detail-item"
							v-if="transactionDetails.bookingCode"
						>
							<span class="detail-label">Mã đặt vé:</span>
							<span class="detail-value">{{
								transactionDetails.bookingCode
							}}</span>
						</div>
					</div>
				</div>
			</transition>

			<!-- Action Buttons -->
			<transition name="slide-up" appear>
				<div class="action-buttons">
					<button @click="retryPayment" class="btn btn-primary">
						<RefreshCw class="btn-icon" />
						Thử Lại
					</button>
					<button
						@click="chooseOtherMethod"
						class="btn btn-secondary"
					>
						<CreditCard class="btn-icon" />
						Phương Thức Khác
					</button>
					<button @click="goToHome" class="btn btn-ghost">
						<Home class="btn-icon" />
						Về Trang Chủ
					</button>
				</div>
			</transition>

			<!-- Support Section -->
			<transition name="fade" appear>
				<div class="support-section">
					<Phone class="support-icon" />
					<p class="support-text">
						Cần hỗ trợ? Liên hệ hotline:
						<a href="tel:1900xxxx" class="support-link"
							>1900 XXXX</a
						>
					</p>
				</div>
			</transition>
		</div>

		<!-- Background Animation -->
		<div class="bg-animation">
			<div class="circle circle-1"></div>
			<div class="circle circle-2"></div>
			<div class="circle circle-3"></div>
		</div>
	</div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getResponseInfo } from "@/utils/paymentCodes";
import {
	AlertCircle,
	XCircle,
	CreditCardOff,
	Lock,
	Clock,
	ShieldOff,
	Wallet,
	TrendingUp,
	Tool,
	AlertOctagon,
	RefreshCw,
	CreditCard,
	Home,
	Phone,
	AlertTriangle,
} from "lucide-vue-next";

export default {
	name: "PaymentFailed",
	components: {
		AlertCircle,
		XCircle,
		CreditCardOff,
		Lock,
		Clock,
		ShieldOff,
		Wallet,
		TrendingUp,
		Tool,
		AlertOctagon,
		RefreshCw,
		CreditCard,
		Home,
		Phone,
		AlertTriangle,
	},
	setup() {
		const route = useRoute();
		const router = useRouter();

		const errorCode = ref("99");
		const errorMessage = ref("");
		const transactionDetails = ref(null);

		const responseInfo = computed(() => {
			return getResponseInfo(errorCode.value);
		});

		const iconComponent = computed(() => {
			const iconMap = {
				"x-circle": XCircle,
				"credit-card-off": CreditCardOff,
				lock: Lock,
				clock: Clock,
				"shield-off": ShieldOff,
				wallet: Wallet,
				"trending-up": TrendingUp,
				tool: Tool,
				"alert-octagon": AlertOctagon,
				"alert-circle": AlertCircle,
				"alert-triangle": AlertTriangle,
			};
			return iconMap[responseInfo.value.icon] || AlertCircle;
		});

		const formatCurrency = (amount) => {
			return new Intl.NumberFormat("vi-VN", {
				style: "currency",
				currency: "VND",
			}).format(amount);
		};

		const formatDateTime = (timestamp) => {
			return new Date(timestamp).toLocaleString("vi-VN");
		};

		const retryPayment = () => {
			// Logic to retry payment
			if (transactionDetails.value?.bookingCode) {
				router.push(
					`/booking/${transactionDetails.value.bookingCode}/payment`
				);
			} else {
				router.push("/");
			}
		};

		const chooseOtherMethod = () => {
			// Logic to choose other payment method
			if (transactionDetails.value?.bookingCode) {
				router.push(
					`/booking/${transactionDetails.value.bookingCode}/payment-methods`
				);
			}
		};

		const goToHome = () => {
			router.push("/");
		};

		onMounted(() => {
			// Get error code and message from URL params
			errorCode.value = route.query.code || "99";
			errorMessage.value = route.query.message || "";

			// Get transaction details from sessionStorage or API
			const storedDetails = sessionStorage.getItem("lastTransaction");
			if (storedDetails) {
				transactionDetails.value = JSON.parse(storedDetails);
			}

			// Optional: Fetch additional details from API
			if (route.query.transactionId) {
				// fetchTransactionDetails(route.query.transactionId);
			}
		});

		return {
			errorCode,
			errorMessage,
			responseInfo,
			iconComponent,
			transactionDetails,
			formatCurrency,
			formatDateTime,
			retryPayment,
			chooseOtherMethod,
			goToHome,
		};
	},
};
</script>

<style scoped>
.payment-result-container {
	min-height: 100vh;
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 20px;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	position: relative;
	overflow: hidden;
}

.payment-card {
	background: white;
	border-radius: 24px;
	padding: 40px;
	max-width: 600px;
	width: 100%;
	box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
	position: relative;
	z-index: 10;
}

/* Icon Wrapper */
.icon-wrapper {
	display: flex;
	justify-content: center;
	margin-bottom: 24px;
}

.icon-circle {
	width: 120px;
	height: 120px;
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	position: relative;
	animation: pulse 2s infinite;
}

.main-icon {
	width: 60px;
	height: 60px;
	stroke-width: 1.5;
}

/* Error Code Badge */
.error-code-badge {
	position: absolute;
	top: 20px;
	right: 20px;
	color: white;
	padding: 6px 12px;
	border-radius: 20px;
	font-size: 12px;
	font-weight: 600;
	letter-spacing: 0.5px;
}

/* Message Section */
.message-section {
	text-align: center;
	margin-bottom: 32px;
}

.title {
	font-size: 28px;
	font-weight: 700;
	color: #1f2937;
	margin-bottom: 12px;
}

.error-message {
	font-size: 18px;
	color: #6b7280;
	line-height: 1.6;
}

/* Info Section */
.info-section {
	margin-bottom: 32px;
}

.info-card {
	background: #f3f4f6;
	border-radius: 12px;
	padding: 16px;
	display: flex;
	gap: 12px;
}

.info-icon {
	width: 20px;
	height: 20px;
	color: #6b7280;
	flex-shrink: 0;
	margin-top: 2px;
}

.info-text {
	flex: 1;
}

.info-text p {
	color: #4b5563;
	font-size: 14px;
	line-height: 1.6;
	margin-bottom: 8px;
}

.info-text p:last-child {
	margin-bottom: 0;
}

.action-text {
	font-weight: 500;
	color: #374151;
}

/* Details Section */
.details-section {
	background: #f9fafb;
	border-radius: 12px;
	padding: 20px;
	margin-bottom: 32px;
}

.details-title {
	font-size: 16px;
	font-weight: 600;
	color: #374151;
	margin-bottom: 16px;
}

.details-grid {
	display: grid;
	gap: 12px;
}

.detail-item {
	display: flex;
	justify-content: space-between;
	padding: 8px 0;
	border-bottom: 1px solid #e5e7eb;
}

.detail-item:last-child {
	border-bottom: none;
}

.detail-label {
	font-size: 14px;
	color: #6b7280;
}

.detail-value {
	font-size: 14px;
	font-weight: 500;
	color: #1f2937;
}

/* Action Buttons */
.action-buttons {
	display: flex;
	gap: 12px;
	margin-bottom: 24px;
	flex-wrap: wrap;
}

.btn {
	flex: 1;
	min-width: 140px;
	padding: 12px 20px;
	border-radius: 10px;
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
	box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
	background: #f3f4f6;
	color: #4b5563;
}

.btn-secondary:hover {
	background: #e5e7eb;
}

.btn-ghost {
	background: transparent;
	color: #6b7280;
	border: 1px solid #e5e7eb;
}

.btn-ghost:hover {
	background: #f9fafb;
}

/* Support Section */
.support-section {
	text-align: center;
	padding-top: 20px;
	border-top: 1px solid #e5e7eb;
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 8px;
}

.support-icon {
	width: 16px;
	height: 16px;
	color: #6b7280;
}

.support-text {
	font-size: 14px;
	color: #6b7280;
}

.support-link {
	color: #667eea;
	font-weight: 600;
	text-decoration: none;
}

.support-link:hover {
	text-decoration: underline;
}

/* Background Animation */
.bg-animation {
	position: absolute;
	width: 100%;
	height: 100%;
	top: 0;
	left: 0;
	z-index: 1;
}

.circle {
	position: absolute;
	border-radius: 50%;
	background: rgba(255, 255, 255, 0.1);
	animation: float 20s infinite;
}

.circle-1 {
	width: 300px;
	height: 300px;
	top: -150px;
	left: -150px;
	animation-delay: 0s;
}

.circle-2 {
	width: 200px;
	height: 200px;
	bottom: -100px;
	right: -100px;
	animation-delay: 5s;
}

.circle-3 {
	width: 150px;
	height: 150px;
	top: 50%;
	left: 50%;
	animation-delay: 10s;
}

/* Animations */
@keyframes pulse {
	0% {
		box-shadow: 0 0 0 0 currentColor;
	}
	70% {
		box-shadow: 0 0 0 20px rgba(0, 0, 0, 0);
	}
	100% {
		box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
	}
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
.bounce-enter-active {
	animation: bounce-in 0.6s;
}

@keyframes bounce-in {
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
	transform: translateY(20px);
	opacity: 0;
}

/* Responsive */
@media (max-width: 640px) {
	.payment-card {
		padding: 24px;
	}

	.icon-circle {
		width: 100px;
		height: 100px;
	}

	.main-icon {
		width: 50px;
		height: 50px;
	}

	.title {
		font-size: 24px;
	}

	.error-message {
		font-size: 16px;
	}

	.action-buttons {
		flex-direction: column;
	}

	.btn {
		width: 100%;
	}
}

/* Severity Styles */
.severity-warning .icon-circle {
	animation: pulse-warning 2s infinite;
}

.severity-info .icon-circle {
	animation: none;
}

@keyframes pulse-warning {
	0% {
		box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4);
	}
	70% {
		box-shadow: 0 0 0 20px rgba(245, 158, 11, 0);
	}
	100% {
		box-shadow: 0 0 0 0 rgba(245, 158, 11, 0);
	}
}
</style>
