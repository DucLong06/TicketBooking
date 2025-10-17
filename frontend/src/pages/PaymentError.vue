<template>
	<div
		class="relative min-h-screen bg-gradient-to-br from-red-50 via-orange-50 to-pink-50"
	>
		<!-- Background -->
		<div class="absolute inset-0 overflow-hidden">
			<div
				class="absolute w-64 h-64 rounded-full bg-red-200 opacity-20 -top-20 -left-20 animate-pulse"
			></div>
			<div
				class="absolute w-96 h-96 rounded-full bg-orange-200 opacity-20 -bottom-32 -right-32 animate-pulse"
				style="animation-delay: 1s"
			></div>
		</div>

		<!-- Content -->
		<div
			class="relative z-10 flex items-center justify-center min-h-screen px-4"
		>
			<div class="w-full max-w-md text-center">
				<!-- Icon -->
				<div class="flex justify-center mb-8">
					<div class="relative">
						<div
							class="absolute inset-0 bg-red-500 rounded-full opacity-20 animate-ping"
						></div>
						<div
							class="relative flex items-center justify-center w-24 h-24 bg-red-500 rounded-full"
						>
							<svg
								class="w-12 h-12 text-white"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
								></path>
							</svg>
						</div>
					</div>
				</div>

				<!-- Card -->
				<div class="p-8 bg-white shadow-2xl rounded-2xl">
					<h1 class="mb-4 text-3xl font-bold text-red-600">
						Lỗi thanh toán
					</h1>

					<p class="mb-6 text-lg text-gray-600">
						{{ errorReason }}
					</p>

					<!-- Error Details -->
					<div
						class="p-4 mb-6 border-l-4 border-red-500 rounded-r-lg bg-red-50"
					>
						<p class="text-sm text-red-700">
							{{ errorDetails }}
						</p>
					</div>

					<!-- Actions -->
					<div class="space-y-3">
						<button
							@click="goHome"
							class="w-full px-6 py-3 font-semibold text-white transition-all bg-red-600 rounded-lg hover:bg-red-700"
						>
							Về trang chủ
						</button>

						<button
							@click="contactSupport"
							class="w-full px-6 py-3 font-semibold text-gray-700 transition-all border-2 border-gray-300 rounded-lg hover:bg-gray-50"
						>
							Liên hệ hỗ trợ
						</button>
					</div>
				</div>

				<!-- Support Info -->
				<div class="mt-6 text-sm text-gray-600">
					<p>
						Hotline:
						<a class="font-medium text-red-600 hover:underline">{{
							contactInfo.hotline_display
						}}</a>
					</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();
import { useContact } from "@/composables/useContact";

const { contactInfo, fetchContactInfo } = useContact();

onMounted(async () => {});
const errorReason = ref("Có lỗi xảy ra trong quá trình xử lý thanh toán");
const errorDetails = ref(
	"Vui lòng thử lại sau hoặc liên hệ với bộ phận hỗ trợ để được trợ giúp."
);

const errorReasons = {
	invalid_signature:
		"Xác thực không hợp lệ. Giao dịch có thể đã bị can thiệp.",
	parse_error: "Không thể xử lý dữ liệu thanh toán.",
	missing_invoice: "Không tìm thấy thông tin giao dịch.",
	payment_not_found: "Không tìm thấy đơn hàng trong hệ thống.",
	server_error: "Lỗi hệ thống. Vui lòng thử lại sau.",
	timeout: "Phiên thanh toán đã hết hạn.",
};

const errorDetailsMap = {
	invalid_signature:
		"Dữ liệu thanh toán không hợp lệ. Vui lòng không sửa đổi URL trả về.",
	parse_error:
		"Hệ thống không thể đọc thông tin thanh toán từ cổng thanh toán.",
	missing_invoice:
		"Thiếu mã giao dịch. Vui lòng liên hệ hỗ trợ với thông tin đơn hàng.",
	payment_not_found: "Đơn hàng không tồn tại hoặc đã bị hủy.",
	server_error:
		"Có lỗi xảy ra trong hệ thống. Chúng tôi đang xử lý vấn đề này.",
	timeout: "Bạn đã hết thời gian thanh toán. Vui lòng đặt vé lại.",
};

const goHome = () => {
	router.push("/");
};

const contactSupport = () => {
	window.location.href = "mailto:support@example.com";
};

onMounted(async () => {
	await fetchContactInfo();
	const reason = route.query.reason || "unknown";
	errorReason.value = errorReasons[reason] || errorReason.value;
	errorDetails.value = errorDetailsMap[reason] || errorDetails.value;
});
</script>

<style scoped>
@keyframes pulse {
	0%,
	100% {
		opacity: 0.2;
	}
	50% {
		opacity: 0.4;
	}
}

.animate-pulse {
	animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-ping {
	animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;
}

@keyframes ping {
	75%,
	100% {
		transform: scale(2);
		opacity: 0;
	}
}
</style>
