<template>
	<DefaultLayout>
		<PosterSlider />

		<section class="py-16 bg-[#fdfcf0]">
			<div class="container mx-auto px-4">
				<h2
					class="uppercase text-3xl font-bold text-center mb-12 text-[#372e2d]"
				>
					Chương trình đang diễn
				</h2>

				<div v-if="loading" class="text-center py-12">
					<DuongCamLoading
						size="lg"
						message="Đang tải chương trình..."
					/>
				</div>

				<div
					v-else-if="shows.length > 0"
					class="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6"
				>
					<div
						v-for="show in shows"
						:key="show.id"
						class="grid grid-cols-5 bg-[#fdfcf0] rounded-lg overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 border border-[#d8a669]/30"
					>
						<div class="col-span-2">
							<OptimizedImage
								v-if="show.poster"
								:src="show.poster"
								:alt="show.name"
								aspect-ratio="2/3"
								imageClass="w-full h-full object-cover"
							/>
							<div
								v-else
								class="w-full h-full aspect-[2/3] bg-gradient-to-br from-[#d8a669]/20 to-[#372e2d]/20 flex items-center justify-center"
							>
								<svg
									class="w-12 h-12 text-[#d8a669]/30"
									fill="currentColor"
									viewBox="0 0 24 24"
								>
									<path d="M4 4h16v12H4V4m0 14h16v2H4v-2z" />
								</svg>
							</div>
						</div>

						<div
							class="col-span-3 p-4 sm:p-5 flex flex-col justify-between"
						>
							<div class="flex-1">
								<h3
									class="text-lg sm:text-xl lg:text-2xl font-bold text-[#372e2d] mb-3 line-clamp-2 uppercase"
								>
									{{ show.name }}
								</h3>

								<div
									class="flex items-center gap-2 text-[#372e2d]/80 mb-3 text-sm sm:text-base"
								>
									<svg
										class="w-4 h-4 sm:w-5 sm:h-5 flex-shrink-0 text-[#d8a669]"
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
									<span
										class="line-clamp-1 font-medium uppercase"
										>{{ show.venue_name }}</span
									>
								</div>

								<div
									v-if="show.duration_minutes"
									class="flex items-center gap-2 text-[#372e2d]/80 text-sm sm:text-base"
								>
									<svg
										class="w-4 h-4 sm:w-5 sm:h-5 text-[#d8a669]"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
										/>
									</svg>
									<span class="font-medium uppercase"
										>{{ show.duration_minutes }} phút</span
									>
								</div>
							</div>

							<div
								class="flex flex-col gap-2 w-full mt-4 sm:mt-6"
							>
								<button
									@click.stop="goToBookingAndScroll(show.id)"
									class="uppercase font-semibold bg-[#d8a669] text-white rounded-lg shadow-lg hover:bg-[#b8884d] transform hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center gap-2 py-2.5 sm:py-3 text-sm sm:text-base"
								>
									<svg
										class="w-4 h-4 sm:w-5 sm:h-5"
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
									<span>Đặt vé</span>
								</button>

								<button
									@click.stop="goToDetails(show.id)"
									class="uppercase font-semibold bg-white text-[#d8a669] border-2 border-[#d8a669] rounded-lg shadow-lg hover:bg-[#d8a669]/10 transform hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center gap-2 py-2.5 sm:py-3 text-sm sm:text-base"
								>
									<svg
										class="w-4 h-4 sm:w-5 sm:h-5"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
										/>
									</svg>
									<span>Chi tiết</span>
								</button>

								<button
									v-if="show.trailer_url"
									@click.stop="openTrailer(show.trailer_url)"
									class="uppercase font-semibold bg-white text-[#372e2d]/90 border-2 border-[#372e2d]/30 rounded-lg shadow-lg hover:bg-gray-50 transform hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center gap-2 py-2.5 sm:py-3 text-sm sm:text-base"
								>
									<svg
										class="w-4 h-4 sm:w-5 sm:h-5"
										fill="currentColor"
										viewBox="0 0 24 24"
									>
										<path d="M8 5v14l11-7z" />
									</svg>
									<span>Trailer</span>
								</button>
							</div>
						</div>
					</div>
				</div>

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

const goToDetails = (showId) => {
	router.push(`/booking/${showId}`);
};

const goToBookingAndScroll = (showId) => {
	router.push(`/booking/${showId}#performances`);
};

const openTrailer = (url) => {
	if (url) {
		currentTrailerUrl.value = url;
		showTrailerPopup.value = true;
		document.body.style.overflow = "hidden";
	}
};

const closeTrailer = () => {
	showTrailerPopup.value = false;
	currentTrailerUrl.value = "";
	document.body.style.overflow = "";
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
</style>