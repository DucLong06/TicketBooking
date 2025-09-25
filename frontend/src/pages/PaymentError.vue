<template>
	<div class="error-container">
		<div class="error-card">
			<!-- Error Animation -->
			<div class="error-animation">
				<transition name="shake" appear>
					<div class="error-icon-wrapper">
						<AlertTriangle class="error-icon" />
					</div>
				</transition>
			</div>

			<!-- Error Message -->
			<transition name="fade" appear>
				<div class="message-section">
					<h1 class="title">Đã Xảy Ra Lỗi</h1>
					<p class="subtitle">
						Chúng tôi không thể xử lý yêu cầu của bạn. Vui lòng thử
						lại sau.
					</p>
				</div>
			</transition>

			<!-- Error Details -->
			<transition name="slide-up" appear>
				<div class="error-details">
					<div class="detail-card">
						<AlertCircle class="detail-icon" />
						<div class="detail-content">
							<h3 class="detail-title">Nguyên nhân có thể:</h3>
							<ul class="detail-list">
								<li>Phiên làm việc đã hết hạn</li>
								<li>Kết nối mạng không ổn định</li>
								<li>Thông tin giao dịch không hợp lệ</li>
								<li>Hệ thống đang bảo trì</li>
							</ul>
						</div>
					</div>
				</div>
			</transition>

			<!-- Action Buttons -->
			<transition name="slide-up" appear>
				<div class="action-section">
					<button @click="goBack" class="btn btn-primary">
						<ArrowLeft class="btn-icon" />
						Quay Lại
					</button>
					<button @click="goToHome" class="btn btn-secondary">
						<Home class="btn-icon" />
						Về Trang Chủ
					</button>
				</div>
			</transition>

			<!-- Support Info -->
			<transition name="fade" appear>
				<div class="support-info">
					<HelpCircle class="support-icon" />
					<p class="support-text">
						Nếu vấn đề vẫn tiếp tục, vui lòng liên hệ
						<a href="tel:1900xxxx" class="support-link"
							>1900 XXXX</a
						>
					</p>
				</div>
			</transition>

			<!-- Error Code (if available) -->
			<div class="error-code" v-if="errorCode">
				Mã lỗi: {{ errorCode }}
			</div>
		</div>

		<!-- Background Pattern -->
		<div class="bg-pattern">
			<div class="pattern-line pattern-line-1"></div>
			<div class="pattern-line pattern-line-2"></div>
			<div class="pattern-line pattern-line-3"></div>
		</div>
	</div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
	AlertTriangle,
	AlertCircle,
	ArrowLeft,
	Home,
	HelpCircle,
} from "lucide-vue-next";

export default {
	name: "PaymentError",
	components: {
		AlertTriangle,
		AlertCircle,
		ArrowLeft,
		Home,
		HelpCircle,
	},
	setup() {
		const route = useRoute();
		const router = useRouter();
		const errorCode = ref("");

		const goBack = () => {
			router.back();
		};

		const goToHome = () => {
			router.push("/");
		};

		onMounted(() => {
			// Get error code from query params if available
			errorCode.value = route.query.code || "";
		});

		return {
			errorCode,
			goBack,
			goToHome,
		};
	},
};
</script>

<style scoped>
.error-container {
	min-height: 100vh;
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 20px;
	background: linear-gradient(135deg, #374151 0%, #1f2937 100%);
	position: relative;
	overflow: hidden;
}

.error-card {
	background: white;
	border-radius: 24px;
	padding: 48px;
	max-width: 500px;
	width: 100%;
	box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
	position: relative;
	z-index: 10;
}

/* Error Animation */
.error-animation {
	display: flex;
	justify-content: center;
	margin-bottom: 32px;
}

.error-icon-wrapper {
	width: 100px;
	height: 100px;
	background: linear-gradient(135deg, #fef2f2, #fee2e2);
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	position: relative;
}

.error-icon-wrapper::before {
	content: "";
	position: absolute;
	width: 100%;
	height: 100%;
	border-radius: 50%;
	background: linear-gradient(135deg, #ef4444, #dc2626);
	opacity: 0.1;
	animation: pulse 2s infinite;
}

.error-icon {
	width: 50px;
	height: 50px;
	color: #ef4444;
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

.subtitle {
	font-size: 16px;
	color: #6b7280;
	line-height: 1.6;
}

/* Error Details */
.error-details {
	margin-bottom: 32px;
}

.detail-card {
	background: #f9fafb;
	border-radius: 12px;
	padding: 20px;
	display: flex;
	gap: 16px;
}

.detail-icon {
	width: 24px;
	height: 24px;
	color: #f59e0b;
	flex-shrink: 0;
	margin-top: 2px;
}

.detail-content {
	flex: 1;
}

.detail-title {
	font-size: 16px;
	font-weight: 600;
	color: #374151;
	margin-bottom: 12px;
}

.detail-list {
	list-style: none;
	padding: 0;
	margin: 0;
}

.detail-list li {
	font-size: 14px;
	color: #6b7280;
	padding: 6px 0;
	padding-left: 20px;
	position: relative;
}

.detail-list li::before {
	content: "•";
	position: absolute;
	left: 0;
	color: #9ca3af;
}

/* Action Buttons */
.action-section {
	display: flex;
	gap: 12px;
	margin-bottom: 32px;
}

.btn {
	flex: 1;
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
	background: linear-gradient(135deg, #374151, #1f2937);
	color: white;
}

.btn-primary:hover {
	transform: translateY(-2px);
	box-shadow: 0 10px 25px rgba(55, 65, 81, 0.3);
}

.btn-secondary {
	background: #f3f4f6;
	color: #4b5563;
}

.btn-secondary:hover {
	background: #e5e7eb;
}

/* Support Info */
.support-info {
	text-align: center;
	padding-top: 24px;
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
	color: #374151;
	font-weight: 600;
	text-decoration: none;
}

.support-link:hover {
	text-decoration: underline;
}

/* Error Code */
.error-code {
	position: absolute;
	bottom: 20px;
	right: 20px;
	font-size: 12px;
	color: #9ca3af;
	font-family: "Courier New", monospace;
}

/* Background Pattern */
.bg-pattern {
	position: absolute;
	width: 100%;
	height: 100%;
	top: 0;
	left: 0;
	z-index: 1;
	overflow: hidden;
}

.pattern-line {
	position: absolute;
	background: linear-gradient(
		90deg,
		transparent,
		rgba(255, 255, 255, 0.03),
		transparent
	);
	animation: drift 20s infinite linear;
}

.pattern-line-1 {
	width: 200%;
	height: 2px;
	top: 20%;
	left: -100%;
}

.pattern-line-2 {
	width: 200%;
	height: 2px;
	top: 50%;
	left: -100%;
	animation-delay: 5s;
}

.pattern-line-3 {
	width: 200%;
	height: 2px;
	top: 80%;
	left: -100%;
	animation-delay: 10s;
}

@keyframes drift {
	0% {
		transform: translateX(0);
	}
	100% {
		transform: translateX(100%);
	}
}

/* Animations */
@keyframes pulse {
	0% {
		transform: scale(1);
		opacity: 0.1;
	}
	50% {
		transform: scale(1.2);
		opacity: 0.05;
	}
	100% {
		transform: scale(1);
		opacity: 0.1;
	}
}

.shake-enter-active {
	animation: shake 0.6s;
}

@keyframes shake {
	0%,
	100% {
		transform: translateX(0);
	}
	10%,
	30%,
	50%,
	70%,
	90% {
		transform: translateX(-10px);
	}
	20%,
	40%,
	60%,
	80% {
		transform: translateX(10px);
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
	.error-card {
		padding: 32px 24px;
	}

	.title {
		font-size: 24px;
	}

	.subtitle {
		font-size: 15px;
	}

	.action-section {
		flex-direction: column;
	}

	.btn {
		width: 100%;
	}

	.error-icon-wrapper {
		width: 80px;
		height: 80px;
	}

	.error-icon {
		width: 40px;
		height: 40px;
	}
}
</style>
