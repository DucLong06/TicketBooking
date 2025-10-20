<template>
	<div class="relative w-full overflow-hidden bg-gray-900">
		<!-- Loading State -->
		<div
			v-if="loading"
			class="w-full aspect-[3/1] flex items-center justify-center bg-gray-800"
		>
			<DuongCamLoading size="lg" message="Đang tải poster..." />
		</div>

		<!-- Slider Container -->
		<div
			v-else-if="posters.length > 0"
			class="relative w-full aspect-[3/1]"
			@touchstart="handleTouchStart"
			@touchmove="handleTouchMove"
			@touchend="handleTouchEnd"
		>
			<!-- Slides -->
			<TransitionGroup name="slide">
				<div
					v-for="(poster, index) in posters"
					v-show="index === currentSlide"
					:key="poster.id"
					class="absolute inset-0 w-full h-full"
				>
					<a
						:href="`/booking/${poster.show_id}`"
						@click.prevent="goToShow(poster.show_id)"
						class="block w-full h-full cursor-pointer group"
					>
						<div class="relative w-full h-full overflow-hidden">
							<img
								:src="poster.image"
								:alt="poster.title"
								:loading="getLoadingStrategy(index)"
								:fetchpriority="index === 0 ? 'high' : 'low'"
								decoding="async"
								class="w-full h-full object-cover object-center transition-transform duration-700 group-hover:scale-105"
								@load="onImageLoad(index)"
								@error="onImageError(index)"
							/>

							<div
								v-if="
									!loadedImages[index] && !errorImages[index]
								"
								class="absolute inset-0 bg-gradient-to-br from-gray-800 via-gray-700 to-gray-900 animate-pulse"
							>
								<div
									class="absolute inset-0 flex items-center justify-center"
								>
									<DuongCamLoading
										size="lg"
										:show-branding="false"
									/>
								</div>
							</div>

							<!-- Error fallback -->
							<div
								v-if="errorImages[index]"
								class="absolute inset-0 bg-gradient-to-br from-red-900/20 to-gray-900 flex items-center justify-center"
							>
								<div class="text-center text-white/70">
									<svg
										class="w-20 h-20 mx-auto mb-2"
										fill="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											d="M4 4h16v12H4V4m0 14h16v2H4v-2z"
										/>
									</svg>
									<p>Không thể tải ảnh</p>
								</div>
							</div>

							<!-- Gradient overlay -->
							<div
								class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent"
							></div>

							<!-- Content overlay -->
							<div
								class="absolute bottom-0 left-0 right-0 p-4 md:p-8 lg:p-12"
							>
								<button
									class="hidden md:block mt-4 bg-[#d8a669] uppercase text-white px-6 py-3 rounded-lg font-semibold hover:bg-[#b8884d] hover:scale-105 transition shadow-lg"
								>
									Đặt vé ngay
								</button>
							</div>
						</div>
					</a>
				</div>
			</TransitionGroup>

			<!-- Navigation Arrows - Desktop only -->
			<button
				v-if="posters.length > 1"
				@click="prevSlide"
				class="hidden md:flex absolute left-4 top-1/2 -translate-y-1/2 bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white p-3 rounded-full transition z-10 items-center justify-center"
				aria-label="Previous slide"
			>
				<svg
					class="w-6 h-6"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M15 19l-7-7 7-7"
					/>
				</svg>
			</button>
			<button
				v-if="posters.length > 1"
				@click="nextSlide"
				class="hidden md:flex absolute right-4 top-1/2 -translate-y-1/2 bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white p-3 rounded-full transition z-10 items-center justify-center"
				aria-label="Next slide"
			>
				<svg
					class="w-6 h-6"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M9 5l7 7-7 7"
					/>
				</svg>
			</button>

			<!-- Dots indicator -->
			<div
				v-if="posters.length > 1"
				class="absolute bottom-4 md:bottom-6 left-1/2 -translate-x-1/2 flex space-x-2 z-10"
			>
				<button
					v-for="(poster, index) in posters"
					:key="`dot-${poster.id}`"
					@click="goToSlide(index)"
					:class="[
						'h-2 rounded-full transition-all duration-300',
						index === currentSlide
							? 'bg-[#d8a669] w-8'
							: 'bg-white/50 hover:bg-white/75 w-2',
					]"
					:aria-label="`Go to slide ${index + 1}`"
				></button>
			</div>
		</div>

		<!-- Empty state -->
		<div
			v-else
			class="w-full aspect-[3/1] bg-gradient-to-r from-[#d8a669] to-[#b8884d] flex items-center justify-center text-white"
		>
			<div class="text-center px-4">
				<h2 class="text-2xl md:text-4xl font-bold mb-4">
					Chào mừng đến với Dương Cầm ART
				</h2>
				<p class="text-base md:text-xl">
					Trải nghiệm nghệ thuật đỉnh cao
				</p>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useRouter } from "vue-router";
import { posterAPI } from "../api/poster";
import DuongCamLoading from "@/components/common/DuongCamLoading.vue";

const router = useRouter();
const posters = ref([]);
const currentSlide = ref(0);
const loading = ref(true);
const loadedImages = ref({});
const errorImages = ref({});
let autoPlayInterval = null;

let touchStartX = 0;
let touchEndX = 0;

const getLoadingStrategy = (index) => {
	if (index === 0 || index === 1) {
		return "eager";
	}
	if (index === (currentSlide.value + 1) % posters.value.length) {
		return "eager";
	}
	return "lazy";
};

const onImageLoad = (index) => {
	loadedImages.value[index] = true;
};

const onImageError = (index) => {
	errorImages.value[index] = true;
	console.error(`Failed to load poster at index ${index}`);
};

const goToShow = (showId) => {
	router.push(`/booking/${showId}`);
};

const nextSlide = () => {
	if (posters.value.length > 1) {
		currentSlide.value = (currentSlide.value + 1) % posters.value.length;
		resetAutoPlay();
		preloadNextImage();
	}
};

const prevSlide = () => {
	if (posters.value.length > 1) {
		currentSlide.value =
			currentSlide.value === 0
				? posters.value.length - 1
				: currentSlide.value - 1;
		resetAutoPlay();
		preloadNextImage();
	}
};

const goToSlide = (index) => {
	currentSlide.value = index;
	resetAutoPlay();
	preloadNextImage();
};

const preloadNextImage = () => {
	const nextIndex = (currentSlide.value + 1) % posters.value.length;
	const prevIndex =
		currentSlide.value === 0
			? posters.value.length - 1
			: currentSlide.value - 1;

	[nextIndex, prevIndex].forEach((index) => {
		if (posters.value[index] && !loadedImages.value[index]) {
			const img = new Image();
			img.src = posters.value[index].image;
			img.onload = () => {
				loadedImages.value[index] = true;
			};
		}
	});
};

const startAutoPlay = () => {
	if (posters.value.length > 1) {
		autoPlayInterval = setInterval(() => {
			nextSlide();
		}, 5000);
	}
};

const stopAutoPlay = () => {
	if (autoPlayInterval) {
		clearInterval(autoPlayInterval);
		autoPlayInterval = null;
	}
};

const resetAutoPlay = () => {
	stopAutoPlay();
	startAutoPlay();
};

// Touch handlers for mobile swipe
const handleTouchStart = (e) => {
	touchStartX = e.touches[0].clientX;
	stopAutoPlay();
};

const handleTouchMove = (e) => {
	touchEndX = e.touches[0].clientX;
};

const handleTouchEnd = () => {
	const swipeThreshold = 50;
	const diff = touchStartX - touchEndX;

	if (Math.abs(diff) > swipeThreshold) {
		if (diff > 0) {
			nextSlide();
		} else {
			prevSlide();
		}
	}

	touchStartX = 0;
	touchEndX = 0;
	startAutoPlay();
};

watch(currentSlide, () => {
	preloadNextImage();
});

onMounted(async () => {
	try {
		const response = await posterAPI.getPosters();

		const results = response.data?.results;
		const data = response.data;

		if (Array.isArray(results)) {
			posters.value = results;
		} else if (Array.isArray(data)) {
			posters.value = data;
		} else {
			posters.value = [];
			console.warn(
				"API response for posters was not a valid array:",
				response.data
			);
		}

		if (posters.value.length > 0) {
			[0, 1].forEach((index) => {
				if (posters.value[index]) {
					const img = new Image();
					img.src = posters.value[index].image;
					img.onload = () => {
						loadedImages.value[index] = true;
					};
					img.onerror = () => {
						errorImages.value[index] = true;
					};
				}
			});

			startAutoPlay();
		}
	} catch (error) {
		console.error("Failed to load posters:", error);
		posters.value = [];
	} finally {
		loading.value = false;
	}
});

onUnmounted(() => {
	stopAutoPlay();
});
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
	transition: all 0.8s ease-in-out;
}

.slide-enter-from {
	opacity: 0;
	transform: translateX(100%);
}

.slide-leave-to {
	opacity: 0;
	transform: translateX(-100%);
}

/* Optimize image rendering */
img {
	image-rendering: -webkit-optimize-contrast;
	image-rendering: crisp-edges;
}
</style>
