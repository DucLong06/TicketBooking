<template>
	<DefaultLayout>
		<!-- Hero Section -->
		<section
			class="bg-gradient-to-r from-primary-600 to-primary-700 text-white py-20"
		>
			<div class="container mx-auto px-4 text-center">
				<h1 class="text-4xl md:text-5xl font-bold mb-4">
					Chào mừng đến với Hồ Gươm Opera
				</h1>
				<p class="text-xl mb-8">
					Trải nghiệm nghệ thuật đỉnh cao tại Hà Nội
				</p>
				<button
					class="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
				>
					Xem lịch diễn
				</button>
			</div>
		</section>

		<section class="py-16">
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
					v-else
					class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
				>
					<div
						v-for="show in shows"
						:key="show.id"
						class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition"
					>
						<div class="h-48 bg-gray-300">
							<img
								v-if="show.poster"
								:src="show.poster"
								:alt="show.name"
								class="w-full h-full object-cover"
							/>
						</div>
						<div class="p-6">
							<h3 class="text-xl font-semibold mb-2">
								{{ show.name }}
							</h3>
							<p class="text-gray-600 mb-4">
								{{ show.category }}
							</p>
							<div class="flex justify-between items-center">
								<!-- <span class="text-primary-600 font-bold">
									{{ formatPrice(show.min_price) }} -
									{{ formatPrice(show.max_price) }}
								</span> -->
								<button
									@click="goToBooking(show.id)"
									class="bg-primary-600 text-white px-4 py-2 rounded hover:bg-primary-700 transition"
								>
									Đặt vé
								</button>
							</div>
						</div>
					</div>
				</div>

				<!-- No shows -->
				<div
					v-if="!loading && shows.length === 0"
					class="text-center text-gray-500"
				>
					Không có chương trình nào đang diễn
				</div>
			</div>
		</section>
	</DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import DefaultLayout from "../layouts/DefaultLayout.vue";
import { useBookingStore } from "../stores/booking";

const router = useRouter();
const bookingStore = useBookingStore();

const shows = ref([]);
const loading = ref(true);

const formatPrice = (price) => {
	return new Intl.NumberFormat("vi-VN", {
		style: "currency",
		currency: "VND",
	}).format(price || 0);
};

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
