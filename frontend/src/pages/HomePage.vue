<template>
	<DefaultLayout>
		<!-- Poster Slider Section -->
		<PosterSlider />

		<!-- Shows Section -->
		<section class="py-16 bg-[#fdfcf0]">
			<div class="container mx-auto px-4">
				<h2
					class="uppercase text-3xl font-bold text-center mb-12 text-[#372e2d]"
				>
					Chương trình đang diễn
				</h2>

				<!-- Loading -->
				<div v-if="loading" class="text-center py-12">
					<DuongCamLoading
						size="lg"
						message="Đang tải chương trình..."
					/>
				</div>

				<!-- Shows Grid -->
				<div
					v-else-if="shows.length > 0"
					class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6"
				>
					<div
						v-for="show in shows"
						:key="show.id"
						class="group relative rounded-lg overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 cursor-pointer aspect-[2/3]"
					>
						<!-- Background Image -->
						<div class="absolute inset-0">
							<OptimizedImage
								v-if="show.poster"
								:src="show.poster"
								:alt="show.name"
								aspect-ratio="2/3"
								imageClass="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
							/>
							<!-- <img
								v-if="show.poster"
								:src="show.poster"
								:alt="show.name"
								class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
							/> -->
							<div
								v-else
								class="w-full h-full bg-gradient-to-br from-[#d8a669]/20 to-[#372e2d]/20 flex items-center justify-center"
							>
								<svg
									class="w-16 h-16 text-[#d8a669]/30"
									fill="currentColor"
									viewBox="0 0 24 24"
								>
									<path d="M4 4h16v12H4V4m0 14h16v2H4v-2z" />
								</svg>
							</div>
						</div>

						<!-- Gradient Overlay - Hidden by default, show on hover -->
						<div
							class="absolute inset-0 bg-gradient-to-t from-black via-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
						></div>

						<!-- Content - Only show on hover -->
						<div
							class="absolute inset-0 flex flex-col items-center justify-center p-4 opacity-0 group-hover:opacity-100 transition-all duration-300 z-20"
						>
							<!-- Show Title -->
							<h3
								class="text-white font-bold text-base md:text-lg lg:text-xl mb-3 text-center line-clamp-2 drop-shadow-lg transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300"
							>
								{{ show.name }}
							</h3>

							<!-- Venue Info -->
							<div
								class="uppercase flex items-center gap-2 text-white/90 text-sm md:text-base mb-6 transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300 delay-75"
							>
								<svg
									class="w-4 h-4 md:w-5 md:h-5 flex-shrink-0"
									fill="none"
									stroke="currentColor"
									viewBox="0 0 24 24"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
									/>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
									/>
								</svg>
								<span class="line-clamp-1">{{
									show.venue_name
								}}</span>
							</div>

							<!-- Action Buttons -->
							<div
								class="flex flex-col gap-3 w-full max-w-[200px] transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300 delay-100"
							>
								<button
									@click.stop="goToBooking(show.id)"
									class="w-full uppercase bg-[#d8a669] text-white px-4 py-3 rounded-lg font-bold text-sm md:text-base shadow-xl hover:bg-[#b8884d] transform hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center gap-2"
								>
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
											d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"
										/>
									</svg>
									Đặt vé ngay
								</button>

								<button
									v-if="show.trailer_url"
									@click.stop="openTrailer(show.trailer_url)"
									class="uppercase w-full bg-white/90 backdrop-blur-sm text-[#372e2d] px-4 py-3 rounded-lg font-bold text-sm md:text-base shadow-xl hover:bg-white transform hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center gap-2"
								>
									<svg
										class="w-5 h-5"
										fill="currentColor"
										viewBox="0 0 24 24"
									>
										<path d="M8 5v14l11-7z" />
									</svg>
									Xem Trailer
								</button>
							</div>
						</div>
					</div>
				</div>

				<!-- No shows -->
				<div v-else class="text-center text-[#372e2d] py-12">
					<svg
						class="w-16 h-16 mx-auto mb-4 text-gray-400"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
						/>
					</svg>
					<p class="text-lg">Không có chương trình nào đang diễn</p>
				</div>
			</div>
		</section>

		<!-- Trailer Popup -->
		<TrailerPopup
			:show="showTrailerPopup"
			:trailerUrl="currentTrailerUrl"
			@close="closeTrailer"
		/>
	</DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import DefaultLayout from "../layouts/DefaultLayout.vue";
import PosterSlider from "../components/PosterSlider.vue";
import TrailerPopup from "../components/TrailerPopup.vue";
import { useBookingStore } from "../stores/booking";
import OptimizedImage from "@/components/OptimizedImage.vue";
import DuongCamLoading from "@/components/common/DuongCamLoading.vue";

const router = useRouter();
const bookingStore = useBookingStore();
const shows = ref([]);
const loading = ref(true);

// Trailer popup state
const showTrailerPopup = ref(false);
const currentTrailerUrl = ref("");

const goToBooking = (showId) => {
	router.push(`/booking/${showId}`);
};

const openTrailer = (url) => {
	if (url) {
		currentTrailerUrl.value = url;
		showTrailerPopup.value = true;
		// Prevent body scroll when popup is open
		document.body.style.overflow = "hidden";
	}
};

const closeTrailer = () => {
	showTrailerPopup.value = false;
	currentTrailerUrl.value = "";
	// Restore body scroll
	document.body.style.overflow = "";
};

const formatPrice = (price) => {
	if (!price) return "0đ";
	return new Intl.NumberFormat("vi-VN", {
		style: "currency",
		currency: "VND",
		minimumFractionDigits: 0,
	}).format(price);
};

onMounted(async () => {
	try {
		await bookingStore.loadShows();
		shows.value = bookingStore.shows;
	} catch (error) {
		console.error("Failed to load shows:", error);
	} finally {
		loading.value = false;
	}
});
</script>

<style scoped>
/* Line clamp utility */
.line-clamp-1 {
	display: -webkit-box;
	-webkit-line-clamp: 1;
	-webkit-box-orient: vertical;
	overflow: hidden;
}

.line-clamp-2 {
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	overflow: hidden;
}

/* Ensure proper aspect ratio on all screen sizes */
.aspect-\[2\/3\] {
	aspect-ratio: 2/3;
}
</style>
