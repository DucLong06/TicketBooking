<template>
	<DefaultLayout>
		<!-- Poster Slider Section -->
		<PosterSlider />

		<!-- Shows Section -->
		<section class="py-16 bg-gray-50">
			<div class="container mx-auto px-4">
				<h2 class="text-3xl font-bold text-center mb-12">
					Chương trình đang diễn
				</h2>

				<!-- Loading -->
				<div v-if="loading" class="text-center">
					<div
						class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"
					></div>
				</div>

				<!-- Shows Grid -->
				<div
					v-else-if="shows.length > 0"
					class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
				>
					<div
						v-for="show in shows"
						:key="show.id"
						class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition cursor-pointer"
						@click="goToBooking(show.id)"
					>
						<div
							class="relative h-64 bg-gray-300 overflow-hidden group"
						>
							<img
								v-if="show.poster"
								:src="show.poster"
								:alt="show.name"
								class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
							/>
							<div
								class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"
							></div>
						</div>
						<div class="p-6">
							<h3 class="text-xl font-semibold mb-2">
								{{ show.name }}
							</h3>
							<p class="text-gray-600 mb-4 flex items-center">
								<svg
									class="w-5 h-5 mr-2"
									fill="none"
									stroke="currentColor"
									viewBox="0 0 24 24"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
									/>
								</svg>
								{{ show.category }}
							</p>
							<div class="flex justify-between items-center">
								<button
									@click.stop="goToBooking(show.id)"
									class="bg-gradient-to-r from-pink-600 via-red-500 to-orange-500 text-white px-6 py-3 rounded-lg hover:shadow-lg transition font-semibold"
								>
									Đặt vé ngay
								</button>
							</div>
						</div>
					</div>
				</div>

				<!-- No shows -->
				<div v-else class="text-center text-gray-500 py-12">
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
	</DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import DefaultLayout from "../layouts/DefaultLayout.vue";
import PosterSlider from "../components/PosterSlider.vue";
import { useBookingStore } from "../stores/booking";

const router = useRouter();
const bookingStore = useBookingStore();
const shows = ref([]);
const loading = ref(true);

const goToBooking = (showId) => {
	router.push(`/booking/${showId}`);
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
