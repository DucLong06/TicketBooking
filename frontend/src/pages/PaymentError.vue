<template>
	<div
		class="relative flex items-center justify-center min-h-screen p-5 overflow-hidden bg-gradient-to-br from-slate-700 to-slate-800"
	>
		<div
			class="relative z-10 w-full max-w-lg p-12 bg-white rounded-3xl shadow-2xl"
		>
			<div class="flex justify-center mb-8">
				<transition name="shake" appear>
					<div
						class="relative flex items-center justify-center w-24 h-24 rounded-full bg-gradient-to-br from-red-50 to-red-100"
					>
						<div
							class="absolute w-full h-full bg-red-500 rounded-full opacity-10 animate-pulse"
						></div>
						<AlertTriangle class="z-10 w-12 h-12 text-red-500" />
					</div>
				</transition>
			</div>

			<transition name="fade" appear>
				<div class="mb-8 text-center">
					<h1 class="mb-3 text-3xl font-bold text-slate-800">
						Đã Xảy Ra Lỗi
					</h1>
					<p class="leading-relaxed text-slate-500">
						Chúng tôi không thể xử lý yêu cầu của bạn. Vui lòng thử
						lại sau.
					</p>
				</div>
			</transition>

			<transition name="slide-up" appear>
				<div class="mb-8">
					<div class="flex gap-4 p-5 rounded-xl bg-slate-50">
						<AlertCircle class="w-6 h-6 text-yellow-500 shrink-0" />
						<div class="flex-1">
							<h3 class="mb-3 font-semibold text-slate-700">
								Nguyên nhân có thể:
							</h3>
							<ul class="space-y-2">
								<li class="flex items-start">
									<span class="mr-2 text-slate-400">•</span>
									<span class="text-sm text-slate-600"
										>Phiên làm việc đã hết hạn</span
									>
								</li>
								<li class="flex items-start">
									<span class="mr-2 text-slate-400">•</span>
									<span class="text-sm text-slate-600"
										>Kết nối mạng không ổn định</span
									>
								</li>
								<li class="flex items-start">
									<span class="mr-2 text-slate-400">•</span>
									<span class="text-sm text-slate-600"
										>Thông tin giao dịch không hợp lệ</span
									>
								</li>
								<li class="flex items-start">
									<span class="mr-2 text-slate-400">•</span>
									<span class="text-sm text-slate-600"
										>Hệ thống đang bảo trì</span
									>
								</li>
							</ul>
						</div>
					</div>
				</div>
			</transition>

			<transition name="slide-up" appear>
				<div class="flex flex-col gap-3 mb-8 sm:flex-row">
					<button
						@click="goBack"
						class="flex items-center justify-center flex-1 gap-2 px-5 py-3.5 font-semibold text-white transition-all duration-300 transform bg-gradient-to-br from-slate-700 to-slate-800 rounded-xl hover:-translate-y-0.5 hover:shadow-lg"
					>
						<ArrowLeft class="w-5 h-5" />
						Quay Lại
					</button>
					<button
						@click="goToHome"
						class="flex items-center justify-center flex-1 gap-2 px-5 py-3.5 font-semibold text-slate-600 bg-slate-100 rounded-xl hover:bg-slate-200 transition-colors"
					>
						<Home class="w-5 h-5" />
						Về Trang Chủ
					</button>
				</div>
			</transition>

			<transition name="fade" appear>
				<div
					class="flex items-center justify-center gap-2 pt-6 border-t border-slate-200"
				>
					<HelpCircle class="w-4 h-4 text-slate-500" />
					<p class="text-sm text-slate-500">
						Nếu vấn đề vẫn tiếp tục, vui lòng liên hệ
						<a
							href="tel:1900xxxx"
							class="font-semibold text-slate-700 hover:underline"
							>1900 XXXX</a
						>
					</p>
				</div>
			</transition>

			<div
				v-if="errorCode"
				class="absolute bottom-5 right-5 text-xs font-mono text-slate-400"
			>
				Mã lỗi: {{ errorCode }}
			</div>
		</div>

		<div class="absolute top-0 left-0 z-0 w-full h-full overflow-hidden">
			<div class="pattern-line pattern-line-1"></div>
			<div class="pattern-line pattern-line-2"></div>
			<div class="pattern-line pattern-line-3"></div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
	AlertTriangle,
	AlertCircle,
	ArrowLeft,
	Home,
	HelpCircle,
} from "lucide-vue-next";

const router = useRouter();
const route = useRoute();

const errorCode = ref("");

const goBack = () => {
	router.back();
};

const goToHome = () => {
	router.push("/");
};

onMounted(() => {
	errorCode.value = route.query.code || "";
});
</script>

<style scoped>
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
</style>
