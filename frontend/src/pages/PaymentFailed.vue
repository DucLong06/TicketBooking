<template>
	<div
		class="relative flex items-center justify-center min-h-screen p-5 overflow-hidden bg-gradient-to-br from-indigo-500 to-purple-600"
	>
		<div
			class="relative z-10 w-full max-w-2xl p-6 bg-white sm:p-10 rounded-3xl shadow-2xl"
		>
			<div class="flex justify-center mb-6">
				<transition name="bounce" appear>
					<div
						class="icon-circle relative flex items-center justify-center w-24 h-24 sm:w-32 sm:h-32 rounded-full"
						:class="`severity-${responseInfo.severity}`"
						:style="{ backgroundColor: responseInfo.color + '20' }"
					>
						<component
							:is="iconComponent"
							class="w-12 h-12 stroke-[1.5] sm:w-16 sm:h-16"
							:style="{ color: responseInfo.color }"
						/>
					</div>
				</transition>
			</div>

			<div
				class="absolute px-3 py-1.5 text-xs font-semibold tracking-wider text-white rounded-full top-5 right-5"
				:style="{ backgroundColor: responseInfo.color }"
			>
				MÃ LỖI: {{ errorCode }}
			</div>

			<transition name="fade" appear>
				<div class="mb-8 text-center">
					<h1
						class="mb-3 text-2xl font-bold sm:text-3xl text-slate-800"
					>
						Thanh Toán Thất Bại
					</h1>
					<p
						class="text-base leading-relaxed sm:text-lg text-slate-600"
					>
						{{ responseInfo.message }}
					</p>
				</div>
			</transition>

			<transition name="slide-up" appear>
				<div
					class="mb-8"
					v-if="responseInfo.additionalInfo || responseInfo.action"
				>
					<div class="flex gap-3 p-4 rounded-xl bg-slate-100">
						<AlertCircle
							class="w-5 h-5 mt-0.5 text-slate-500 shrink-0"
						/>
						<div class="text-sm text-slate-600">
							<p v-if="responseInfo.additionalInfo">
								{{ responseInfo.additionalInfo }}
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

			<transition name="slide-up" appear>
				<div
					class="p-5 mb-8 rounded-xl bg-slate-50"
					v-if="transactionDetails"
				>
					<h3 class="mb-4 font-semibold text-slate-700">
						Chi tiết giao dịch
					</h3>
					<div class="space-y-3">
						<div
							class="flex justify-between pb-3 text-sm border-b border-slate-200"
						>
							<span class="text-slate-500">Mã giao dịch:</span>
							<span class="font-medium text-slate-800">{{
								transactionDetails.transactionId
							}}</span>
						</div>
						<div
							class="flex justify-between pb-3 text-sm border-b border-slate-200"
						>
							<span class="text-slate-500">Số tiền:</span>
							<span class="font-medium text-slate-800">{{
								formatCurrency(transactionDetails.amount)
							}}</span>
						</div>
						<div
							class="flex justify-between pb-3 text-sm border-b border-slate-200"
						>
							<span class="text-slate-500">Thời gian:</span>
							<span class="font-medium text-slate-800">{{
								formatDateTime(transactionDetails.timestamp)
							}}</span>
						</div>
						<div
							class="flex justify-between text-sm"
							v-if="transactionDetails.bookingCode"
						>
							<span class="text-slate-500">Mã đặt vé:</span>
							<span class="font-medium text-slate-800">{{
								transactionDetails.bookingCode
							}}</span>
						</div>
					</div>
				</div>
			</transition>

			<transition name="slide-up" appear>
				<div class="flex flex-col gap-3 mb-6 sm:flex-row">
					<button
						@click="retryPayment"
						class="flex items-center justify-center flex-1 gap-2 px-5 py-3 font-semibold text-white transition-all duration-300 transform bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg hover:-translate-y-0.5 hover:shadow-lg hover:shadow-indigo-500/50"
					>
						<RefreshCw class="w-5 h-5" />
						Thử Lại
					</button>
					<button
						@click="chooseOtherMethod"
						class="flex items-center justify-center flex-1 gap-2 px-5 py-3 font-semibold text-slate-600 bg-slate-100 rounded-lg hover:bg-slate-200 transition-colors"
					>
						<CreditCard class="w-5 h-5" />
						Phương Thức Khác
					</button>
					<button
						@click="goToHome"
						class="flex items-center justify-center flex-1 gap-2 px-5 py-3 font-semibold border text-slate-500 border-slate-200 rounded-lg hover:bg-slate-50 transition-colors"
					>
						<Home class="w-5 h-5" />
						Về Trang Chủ
					</button>
				</div>
			</transition>

			<transition name="fade" appear>
				<div
					class="flex items-center justify-center gap-2 pt-5 border-t border-slate-200"
				>
					<Phone class="w-4 h-4 text-slate-500" />
					<p class="text-sm text-slate-500">
						Cần hỗ trợ? Liên hệ hotline:
						<a
							href="tel:1900xxxx"
							class="font-semibold text-indigo-500 hover:underline"
							>1900 XXXX</a
						>
					</p>
				</div>
			</transition>
		</div>

		<div class="absolute top-0 left-0 z-0 w-full h-full">
			<div class="circle circle-1"></div>
			<div class="circle circle-2"></div>
			<div class="circle circle-3"></div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
	AlertCircle,
	XCircle,
	Lock,
	Clock,
	ShieldOff,
	Wallet,
	TrendingUp,
	AlertOctagon,
	RefreshCw,
	CreditCard,
	Home,
	Phone,
	AlertTriangle,
} from "lucide-vue-next";

const route = useRoute();
const router = useRouter();

// --- State ---
const errorCode = ref("99");
const errorMessage = ref("");
const transactionDetails = ref(null);

const mockTransactionDetails = {
	transactionId: "TXN123456789",
	amount: 250000,
	timestamp: new Date().toISOString(),
	bookingCode: "BOOKING_ABC123",
};

// --- Computed Properties ---
const responseInfo = computed(() => getResponseInfo(errorCode.value));

const iconComponent = computed(() => {
	const iconMap = {
		"x-circle": XCircle,
		lock: Lock,
		clock: Clock,
		"shield-off": ShieldOff,
		wallet: Wallet,
		"trending-up": TrendingUp,
		"alert-octagon": AlertOctagon,
		"alert-circle": AlertCircle,
		"alert-triangle": AlertTriangle,
	};
	return iconMap[responseInfo.value.icon] || AlertCircle;
});

// --- Helper Functions ---
const formatCurrency = (amount) => {
	return new Intl.NumberFormat("vi-VN", {
		style: "currency",
		currency: "VND",
	}).format(amount);
};
const formatDateTime = (timestamp) => {
	return new Date(timestamp).toLocaleString("vi-VN");
};

// --- Action Handlers ---
const retryPayment = () => {
	if (transactionDetails.value?.bookingCode) {
		router.push(`/booking/${transactionDetails.value.bookingCode}/payment`);
	} else {
		router.push("/"); // Fallback
	}
};

const chooseOtherMethod = () => {
	if (transactionDetails.value?.bookingCode) {
		router.push(
			`/booking/${transactionDetails.value.bookingCode}/payment-methods`
		);
	}
};

const goToHome = () => {
	router.push("/");
};

// --- Lifecycle Hook ---
onMounted(() => {
	errorCode.value = route.query.code || "99";
	errorMessage.value = route.query.message || "";

	const storedDetails = sessionStorage.getItem("lastTransaction");
	if (storedDetails) {
		transactionDetails.value = JSON.parse(storedDetails);
	} else {
		transactionDetails.value = mockTransactionDetails;
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

/* Icon Animation (Pulse) */
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
/* :style="{ '--dynamic-color-alpha': responseInfo.color + '60' }" */

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
