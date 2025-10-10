<template>
	<div class="relative w-full overflow-hidden bg-gray-900">
		<!-- Loading State -->
		<div
			v-if="loading"
			class="w-full h-64 md:h-96 lg:h-[500px] flex items-center justify-center bg-gray-800"
		>
			<div
				class="animate-spin rounded-full h-12 w-12 border-b-2 border-white"
			></div>
		</div>

		<!-- Slider Container -->
		<div
			v-else-if="posters.length > 0"
			class="relative w-full h-64 md:h-96 lg:h-[500px]"
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
						<!-- Image with overlay gradient -->
						<div class="relative w-full h-full overflow-hidden">
							<img
								:src="poster.image"
								:alt="poster.title"
								class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
							/>
							<!-- Gradient overlay -->
							<div
								class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"
							></div>

							<!-- Title overlay -->
							<div
								class="absolute bottom-0 left-0 right-0 p-6 md:p-8 lg:p-12"
							>
								<!-- <h2
									class="text-2xl md:text-4xl lg:text-5xl font-bold text-white mb-2 drop-shadow-lg"
								>
									{{ poster.title }}
								</h2>
								<p
									class="text-lg md:text-xl text-white/90 drop-shadow-lg"
								>
									{{ poster.show_name }}
								</p> -->
								<button
									class="mt-4 bg-white text-gray-900 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition shadow-lg"
								>
									Đặt vé ngay
								</button>
							</div>
						</div>
					</a>
				</div>
			</TransitionGroup>

			<!-- Navigation Arrows - ONLY DESKTOP (hidden on mobile) -->
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

			<!-- Dots Indicator -->
			<div
				v-if="posters.length > 1"
				class="absolute bottom-4 left-1/2 -translate-x-1/2 flex space-x-2 z-10"
			>
				<button
					v-for="(poster, index) in posters"
					:key="`dot-${poster.id}`"
					@click="goToSlide(index)"
					:class="[
						'w-2 h-2 md:w-3 md:h-3 rounded-full transition-all',
						index === currentSlide
							? 'bg-white w-6 md:w-8'
							: 'bg-white/50 hover:bg-white/75',
					]"
					:aria-label="`Go to slide ${index + 1}`"
				></button>
			</div>
		</div>

		<!-- No Posters -->
		<div
			v-else
			class="w-full h-64 md:h-96 bg-gradient-to-r from-primary-600 to-primary-700 flex items-center justify-center text-white"
		>
			<div class="text-center px-4">
				<h2 class="text-3xl md:text-4xl font-bold mb-4">
					Chào mừng đến với Dương Cầm ART
				</h2>
				<p class="text-lg md:text-xl">
					Trải nghiệm nghệ thuật đỉnh cao
				</p>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { posterAPI } from "../api/poster";

const router = useRouter();
const posters = ref([]);
const currentSlide = ref(0);
const loading = ref(true);
let autoPlayInterval = null;

// Touch/Swipe variables
let touchStartX = 0;
let touchEndX = 0;

const goToShow = (showId) => {
	router.push(`/booking/${showId}`);
};

const nextSlide = () => {
	currentSlide.value = (currentSlide.value + 1) % posters.value.length;
	resetAutoPlay();
};

const prevSlide = () => {
	currentSlide.value =
		currentSlide.value === 0
			? posters.value.length - 1
			: currentSlide.value - 1;
	resetAutoPlay();
};

const goToSlide = (index) => {
	currentSlide.value = index;
	resetAutoPlay();
};

const startAutoPlay = () => {
	if (posters.value.length > 1) {
		autoPlayInterval = setInterval(() => {
			nextSlide();
		}, 5000); // Change slide every 5 seconds
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
};

const handleTouchMove = (e) => {
	touchEndX = e.touches[0].clientX;
};

const handleTouchEnd = () => {
	const swipeThreshold = 50; // Minimum distance for swipe
	const diff = touchStartX - touchEndX;

	if (Math.abs(diff) > swipeThreshold) {
		if (diff > 0) {
			// Swipe left - next slide
			nextSlide();
		} else {
			// Swipe right - previous slide
			prevSlide();
		}
	}

	// Reset values
	touchStartX = 0;
	touchEndX = 0;
};

onMounted(async () => {
	try {
		const response = await posterAPI.getPosters();

		if (response.data.results) {
			posters.value = response.data.results; // Has pagination
		} else {
			posters.value = response.data; // No pagination
		}

		console.log("Loaded posters:", posters.value);
		startAutoPlay();
	} catch (error) {
		console.error("Failed to load posters:", error);
	} finally {
		loading.value = false;
	}
});

onUnmounted(() => {
	stopAutoPlay();
});
</script>

<style scoped>
/* Slide transition */
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
</style>
