<template>
	<div
		class="relative min-h-screen bg-gradient-to-br from-[#372e2d] via-[#4a3f3e] to-[#2d2322] overflow-hidden"
	>
		<!-- Animated Background Elements -->
		<div class="absolute inset-0 overflow-hidden">
			<div class="floating-circle circle-1"></div>
			<div class="floating-circle circle-2"></div>
			<div class="floating-circle circle-3"></div>
		</div>

		<!-- Content -->
		<div
			class="relative z-10 flex items-center justify-center min-h-screen px-4 py-12"
		>
			<div class="text-center max-w-2xl w-full">
				<!-- Animated 404 -->
				<div class="mb-8 animate-bounce-slow">
					<h1
						class="text-9xl md:text-[200px] font-bold text-[#d8a669] tracking-wider drop-shadow-2xl"
					>
						404
					</h1>
					<div
						class="h-2 w-32 md:w-48 mx-auto bg-gradient-to-r from-transparent via-[#d8a669] to-transparent rounded-full opacity-60"
					></div>
				</div>

				<!-- Theater Icon -->
				<div class="mb-6 flex justify-center">
					<div class="relative">
						<svg
							class="w-24 h-24 md:w-32 md:h-32 text-[#d8a669] animate-pulse"
							fill="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-5-9c.83 0 1.5-.67 1.5-1.5S7.83 8 7 8s-1.5.67-1.5 1.5S6.17 11 7 11zm5 0c.83 0 1.5-.67 1.5-1.5S12.83 8 12 8s-1.5.67-1.5 1.5.67 1.5 1.5 1.5zm5 0c.83 0 1.5-.67 1.5-1.5S17.83 8 17 8s-1.5.67-1.5 1.5.67 1.5 1.5 1.5zm-5 2.5c-2.33 0-4.31 1.46-5.11 3.5h10.22c-.8-2.04-2.78-3.5-5.11-3.5z"
							/>
						</svg>
						<div
							class="absolute inset-0 bg-[#d8a669] opacity-20 blur-2xl rounded-full"
						></div>
					</div>
				</div>

				<!-- Message -->
				<div class="mb-8 space-y-4">
					<h2 class="text-3xl md:text-4xl font-bold text-white">
						Ối! Trang không tồn tại
					</h2>
					<p
						class="text-lg md:text-xl text-gray-300 leading-relaxed max-w-lg mx-auto"
					>
						Có vẻ như trang bạn đang tìm kiếm đã không còn hoặc chưa
						bao giờ tồn tại. Hãy quay về trang chủ để khám phá các
						buổi diễn tuyệt vời!
					</p>
				</div>

				<!-- Action Buttons -->
				<div
					class="flex flex-col sm:flex-row gap-4 justify-center items-center"
				>
					<a
						href="/"
						class="group relative inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white bg-[#d8a669] rounded-xl shadow-2xl hover:bg-white hover:text-[#372e2d] transition-all duration-300 transform hover:scale-105 overflow-hidden w-full sm:w-auto"
					>
						<span class="relative z-10 flex items-center gap-2">
							<svg
								class="w-5 h-5 transition-transform group-hover:-translate-x-1"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M10 19l-7-7m0 0l7-7m-7 7h18"
								/>
							</svg>
							Về trang chủ
						</span>
						<div
							class="absolute inset-0 bg-gradient-to-r from-[#d8a669] to-[#c89559] opacity-0 group-hover:opacity-100 transition-opacity"
						></div>
					</a>

					<a
						href="/lookup"
						class="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-[#d8a669] bg-transparent border-2 border-[#d8a669] rounded-xl hover:bg-[#d8a669] hover:text-white transition-all duration-300 transform hover:scale-105 w-full sm:w-auto"
					>
						<span class="flex items-center gap-2">
							<svg
								class="w-5 h-5"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
								/>
							</svg>
							Tra cứu vé
						</span>
					</a>
				</div>

				<!-- Error Code -->
				<div class="mt-12 opacity-60">
					<p class="text-sm text-gray-400 font-mono">
						Error Code: PAGE_NOT_FOUND
					</p>
				</div>
			</div>
		</div>

		<!-- Bottom Wave Decoration -->
		<div class="absolute bottom-0 left-0 right-0">
			<svg
				class="w-full h-24 md:h-32 text-[#d8a669] opacity-10"
				preserveAspectRatio="none"
				viewBox="0 0 1200 120"
				fill="currentColor"
			>
				<path
					d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"
				></path>
			</svg>
		</div>
	</div>
</template>

<script setup>
// No logic needed - pure presentational component
</script>

<style scoped>
@keyframes float {
	0%,
	100% {
		transform: translateY(0) scale(1);
	}
	50% {
		transform: translateY(-20px) scale(1.05);
	}
}

@keyframes bounce-slow {
	0%,
	100% {
		transform: translateY(0);
	}
	50% {
		transform: translateY(-10px);
	}
}

.animate-bounce-slow {
	animation: bounce-slow 2s ease-in-out infinite;
}

.floating-circle {
	position: absolute;
	border-radius: 50%;
	background: radial-gradient(
		circle,
		rgba(216, 166, 105, 0.15) 0%,
		rgba(216, 166, 105, 0) 70%
	);
	animation: float 6s ease-in-out infinite;
}

.circle-1 {
	width: 300px;
	height: 300px;
	top: 10%;
	left: -100px;
	animation-delay: 0s;
}

.circle-2 {
	width: 400px;
	height: 400px;
	top: 40%;
	right: -150px;
	animation-delay: 2s;
}

.circle-3 {
	width: 250px;
	height: 250px;
	bottom: 10%;
	left: 30%;
	animation-delay: 4s;
}

/* Mobile optimizations */
@media (max-width: 640px) {
	.floating-circle {
		opacity: 0.5;
	}

	.circle-1 {
		width: 200px;
		height: 200px;
	}
	.circle-2 {
		width: 250px;
		height: 250px;
	}
	.circle-3 {
		width: 150px;
		height: 150px;
	}
}

/* Smooth transitions for all interactive elements */
a,
button {
	-webkit-tap-highlight-color: transparent;
}
</style>
