<template>
	<div
		class="relative min-h-screen bg-gradient-to-br from-red-50 via-orange-50 to-pink-50"
	>
		<!-- Background Animation -->
		<div class="absolute inset-0 overflow-hidden bg-animation">
			<div class="circle circle-1"></div>
			<div class="circle circle-2"></div>
			<div class="circle circle-3"></div>
		</div>

		<!-- Content -->
		<div
			class="relative z-10 flex items-center justify-center min-h-screen px-4 py-12"
		>
			<div class="w-full max-w-md">
				<!-- Icon Animation -->
				<transition name="bounce" appear>
					<div
						class="flex items-center justify-center mb-8"
						:class="`icon-circle severity-${responseInfo.severity}`"
						:style="{
							'--dynamic-color-alpha': responseInfo.color + '60',
						}"
					>
						<div
							class="relative flex items-center justify-center w-24 h-24 rounded-full shadow-2xl"
							:style="{ backgroundColor: responseInfo.color }"
						>
							<component
								:is="responseInfo.icon"
								class="w-12 h-12 text-white"
							/>
						</div>
					</div>
				</transition>

				<!-- Card -->
				<transition name="fade" appear>
					<div
						class="overflow-hidden bg-white shadow-2xl rounded-2xl"
					>
						<div class="p-8">
							<!-- Title -->
							<h1
								class="mb-2 text-3xl font-bold text-center"
								:style="{ color: responseInfo.color }"
							>
								{{ responseInfo.title }}
							</h1>

							<!-- Error Message -->
							<p class="mb-6 text-center text-slate-600">
								{{ errorMessage || responseInfo.message }}
							</p>

							<!-- Error Code Badge -->
							<div class="flex justify-center mb-6">
								<span
									class="px-4 py-2 text-sm font-mono font-semibold rounded-full"
									:style="{
										backgroundColor:
											responseInfo.color + '20',
										color: responseInfo.color,
									}"
								>
									Mã lỗi: {{ errorCode }}
								</span>
							</div>

							<!-- Additional Info -->
							<transition name="fade">
								<div
									v-if="
										responseInfo.additionalInfo ||
										responseInfo.action
									"
									class="p-4 mb-6 border-l-4 rounded-r-lg bg-slate-50"
									:style="{ borderColor: responseInfo.color }"
								>
									<div class="flex items-start space-x-3">
										<AlertCircle
											class="w-5 h-5 mt-0.5 text-slate-500 shrink-0"
										/>
										<div class="text-sm text-slate-600">
											<p
												v-if="
													responseInfo.additionalInfo
												"
											>
												{{
													responseInfo.additionalInfo
												}}
											</p>
											<p
												v-if="responseInfo.action"
												class="mt-1 font-medium text-slate-700"
											>
												{{ responseInfo.action }}
											</p>
										</div>
									</div>
								</div>
							</transition>

							<!-- Transaction Details -->
							<transition name="slide-up" appear>
								<div
									class="p-5 mb-8 rounded-xl bg-slate-50"
									v-if="transactionDetails"
								>
									<h3
										class="mb-4 font-semibold text-slate-700"
									>
										Chi tiết giao dịch
									</h3>
									<div class="space-y-3">
										<div
											class="flex justify-between pb-3 text-sm border-b border-slate-200"
										>
											<span class="text-slate-500"
												>Mã giao dịch:</span
											>
											<span
												class="font-medium text-slate-800"
											>
												{{
													transactionDetails.transactionId
												}}
											</span>
										</div>
										<div
											class="flex justify-between pb-3 text-sm border-b border-slate-200"
										>
											<span class="text-slate-500"
												>Số tiền:</span
											>
											<span
												class="font-medium text-slate-800"
											>
												{{
													formatCurrency(
														transactionDetails.amount
													)
												}}
											</span>
										</div>
										<div
											class="flex justify-between pb-3 text-sm border-b border-slate-200"
										>
											<span class="text-slate-500"
												>Thời gian:</span
											>
											<span
												class="font-medium text-slate-800"
											>
												{{
													formatDateTime(
														transactionDetails.timestamp
													)
												}}
											</span>
										</div>
										<div
											class="flex justify-between text-sm"
											v-if="transactionDetails.method"
										>
											<span class="text-slate-500"
												>Phương thức:</span
											>
											<span
												class="font-medium text-slate-800"
											>
												{{ transactionDetails.method }}
											</span>
										</div>
									</div>
								</div>
							</transition>

							<!-- Action Buttons -->
							<div class="space-y-3">
								<!-- <button
									@click="retryPayment"
									class="w-full px-6 py-3 font-semibold text-white transition-all duration-200 rounded-lg shadow-lg hover:shadow-xl"
									:style="{
										backgroundColor: responseInfo.color,
										'&:hover': {
											transform: 'translateY(-2px)',
										},
									}"
								>
									Thử lại thanh toán
								</button> -->

								<button
									@click="goToHome"
									class="w-full px-6 py-3 font-semibold transition-all duration-200 border-2 rounded-lg text-slate-700 border-slate-300 hover:bg-slate-50"
								>
									Về trang chủ
								</button>
							</div>

							<!-- Support -->
							<div class="mt-6 text-center">
								<p class="text-sm text-slate-500">
									Cần hỗ trợ?
									<a
										href="mailto:support@example.com"
										class="font-medium hover:underline"
										:style="{ color: responseInfo.color }"
									>
										Liên hệ chúng tôi
									</a>
								</p>
							</div>
						</div>
					</div>
				</transition>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { XCircle, AlertCircle, Clock, CreditCard, Ban } from "lucide-vue-next";

const router = useRouter();
const route = useRoute();

const errorCode = ref("");
const errorMessage = ref("");
const transactionDetails = ref(null);

// 9Pay Error Codes Mapping
const ninepayErrors = {
	"000": {
		title: "Giao dịch thành công",
		message: "Thanh toán của bạn đã được xử lý thành công",
		severity: "success",
		color: "#10b981",
		icon: "CheckCircle",
	},
	"001": {
		title: "Giao dịch thất bại",
		message: "Giao dịch không thành công",
		severity: "error",
		color: "#ef4444",
		icon: XCircle,
		additionalInfo: "Vui lòng kiểm tra lại thông tin thẻ và thử lại.",
	},
	"002": {
		title: "Giao dịch bị từ chối",
		message: "Ngân hàng từ chối giao dịch",
		severity: "error",
		color: "#ef4444",
		icon: Ban,
		additionalInfo: "Vui lòng liên hệ ngân hàng để biết thêm chi tiết.",
	},
	"003": {
		title: "Thẻ không hợp lệ",
		message: "Thông tin thẻ không chính xác",
		severity: "error",
		color: "#ef4444",
		icon: CreditCard,
		additionalInfo: "Vui lòng kiểm tra lại số thẻ, ngày hết hạn và CVV.",
	},
	"004": {
		title: "Không đủ số dư",
		message: "Tài khoản không đủ số dư để thực hiện giao dịch",
		severity: "error",
		color: "#f59e0b",
		icon: AlertCircle,
		additionalInfo: "Vui lòng nạp thêm tiền hoặc sử dụng phương thức khác.",
	},
	"005": {
		title: "Hết hạn giao dịch",
		message: "Phiên giao dịch đã hết hạn",
		severity: "warning",
		color: "#f59e0b",
		icon: Clock,
		additionalInfo: "Vui lòng tạo giao dịch mới.",
	},
	"006": {
		title: "Quá số lần thử",
		message: "Bạn đã nhập sai thông tin quá nhiều lần",
		severity: "error",
		color: "#ef4444",
		icon: Ban,
		additionalInfo: "Vui lòng đợi ít nhất 15 phút trước khi thử lại.",
	},
	"007": {
		title: "Lỗi hệ thống",
		message: "Có lỗi xảy ra từ cổng thanh toán",
		severity: "error",
		color: "#ef4444",
		icon: AlertCircle,
		additionalInfo: "Vui lòng thử lại sau ít phút.",
	},
	"008": {
		title: "Giao dịch bị hủy",
		message: "Bạn đã hủy giao dịch",
		severity: "warning",
		color: "#f59e0b",
		icon: XCircle,
	},
	99: {
		title: "Lỗi không xác định",
		message: "Có lỗi không xác định xảy ra",
		severity: "error",
		color: "#ef4444",
		icon: AlertCircle,
		additionalInfo: "Vui lòng liên hệ bộ phận hỗ trợ.",
	},
};

// Computed
const responseInfo = computed(() => {
	return ninepayErrors[errorCode.value] || ninepayErrors["99"];
});

// Methods
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
	if (transactionDetails.value?.bookingCode) {
		router.push(`/booking/${transactionDetails.value.bookingCode}/payment`);
	} else {
		router.push("/");
	}
};

const goToHome = () => {
	router.push("/");
};

// Lifecycle
onMounted(() => {
	errorCode.value = route.query.code || "99";
	errorMessage.value = route.query.message || "";

	const storedDetails = sessionStorage.getItem("bookingData");
	if (storedDetails) {
		const booking = JSON.parse(storedDetails);
		transactionDetails.value = {
			transactionId: booking.transactionId || "N/A",
			amount: booking.amount || 0,
			timestamp: new Date().toISOString(),
			method: "9Pay",
			bookingCode: booking.bookingCode,
		};
	}
});
</script>

<style scoped>
/* Background Animation */
.bg-animation {
	z-index: 1;
}
.circle {
	position: absolute;
	border-radius: 50%;
	background: rgba(255, 255, 255, 0.08);
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

/* Icon Animation */
.icon-circle.severity-error {
	animation: pulse-error 2s infinite;
}
.icon-circle.severity-warning {
	animation: pulse-warning 2s infinite;
}

@keyframes pulse-error {
	0% {
		box-shadow: 0 0 0 0 var(--dynamic-color-alpha);
	}
	70% {
		box-shadow: 0 0 0 20px rgba(0, 0, 0, 0);
	}
	100% {
		box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
	}
}

@keyframes pulse-warning {
	0% {
		box-shadow: 0 0 0 0 var(--dynamic-color-alpha);
	}
	70% {
		box-shadow: 0 0 0 20px rgba(0, 0, 0, 0);
	}
	100% {
		box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
	}
}

/* Vue Transitions */
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
</style>
