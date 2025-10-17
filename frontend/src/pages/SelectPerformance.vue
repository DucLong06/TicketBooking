<template>
	<DefaultLayout>
		<div class="container mx-auto px-4 py-8">
			<!-- Breadcrumb -->
			<nav class="mb-8">
				<ol class="flex items-center space-x-2 text-sm">
					<li>
						<router-link
							to="/"
							class="text-[#d8a669] hover:text-[#b8884d] font-medium transition"
						>
							Trang chủ
						</router-link>
					</li>
					<li class="text-[#a0866b]">/</li>
					<li class="text-[#372e2d] font-semibold">Chọn suất diễn</li>
				</ol>
			</nav>

			<!-- Loading -->
			<div v-if="loading" class="flex justify-center py-12">
				<div
					class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#d8a669]"
				></div>
			</div>

			<template v-else>
				<!-- Show Info Section -->
				<div
					class="bg-[#fdfcf0] border border-[#d8a669]/30 rounded-lg shadow-lg p-8 mb-8"
				>
					<div class="grid md:grid-cols-3 gap-8">
						<!-- Poster -->
						<div class="md:col-span-1">
							<div
								class="w-full h-80 bg-[#e8dcc8] rounded-lg overflow-hidden border-2 border-[#d8a669]/20"
							>
								<img
									v-if="showInfo.poster"
									:src="showInfo.poster"
									:alt="showInfo.name"
									class="w-full h-full object-cover"
								/>
							</div>
						</div>

						<!-- Show Details -->
						<div class="md:col-span-2">
							<h1 class="text-3xl font-bold mb-4 text-[#372e2d]">
								{{ showInfo.name }}
							</h1>
							<div
								class="space-y-2 text-[#372e2d] mb-6 text-base"
							>
								<p class="font-medium">
									🎭 Thể loại: {{ showInfo.category }}
								</p>
								<p class="font-medium">
									⏱️ Thời lượng:
									{{ showInfo.duration_minutes }} phút
								</p>
								<p class="font-medium">
									📍 Địa điểm: {{ showInfo.venue?.name }}
								</p>
							</div>
							<div class="prose max-w-none">
								<p class="text-[#372e2d] leading-relaxed">
									{{ showInfo.description }}
								</p>
							</div>
						</div>
					</div>
				</div>

				<!-- Performances Section -->
				<div
					class="bg-[#fdfcf0] border border-[#d8a669]/30 rounded-lg shadow-lg p-8"
				>
					<h2 class="text-2xl font-bold mb-6 text-[#372e2d]">
						Chọn suất diễn
					</h2>

					<div
						v-if="performances.length === 0"
						class="text-center text-[#372e2d] py-8"
					>
						Không có suất diễn nào
					</div>

					<div v-else class="space-y-6">
						<!-- Group performances by date -->
						<div
							v-for="(dateGroup, date) in groupedPerformances"
							:key="date"
						>
							<h3
								class="font-semibold text-lg mb-4 text-[#372e2d] flex items-center"
							>
								{{ formatDate(date) }}
							</h3>

							<div
								class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
							>
								<div
									v-for="performance in dateGroup"
									:key="performance.id"
									@click="selectPerformance(performance)"
									:class="[
										'border-2 rounded-lg p-4 text-center cursor-pointer transition-all duration-200',
										{
											'border-[#d8a669] bg-white hover:border-[#b8884d] hover:shadow-md':
												selectedPerformance?.id !==
												performance.id,
											'border-[#372e2d] bg-[#d8a669]/10 shadow-lg ring-2 ring-[#d8a669]':
												selectedPerformance?.id ===
												performance.id,
											'opacity-50 cursor-not-allowed bg-gray-100':
												performance.available_seats ===
												0,
										},
									]"
									:disabled="
										performance.available_seats === 0
									"
								>
									<div
										class="text-lg font-bold text-[#372e2d]"
									>
										{{ formatTime(performance.datetime) }}
									</div>
									<div
										class="text-sm mt-2 font-medium"
										:class="{
											'text-[#372e2d]':
												performance.available_seats > 0,
											'text-red-600':
												performance.available_seats ===
												0,
										}"
									>
										{{
											performance.available_seats > 0
												? `Còn ${performance.available_seats} chỗ`
												: "Hết vé"
										}}
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Continue Button -->
					<div
						v-if="selectedPerformance"
						class="mt-8 flex justify-end"
					>
						<button
							@click="continueToSeatSelection"
							class="bg-[#d8a669] text-white px-8 py-3 rounded-lg font-bold text-lg shadow-lg hover:bg-[#b8884d] hover:shadow-xl transform hover:scale-105 active:scale-95 transition-all duration-200"
						>
							Tiếp tục chọn ghế →
						</button>
					</div>
				</div>
			</template>
		</div>
	</DefaultLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import DefaultLayout from "../layouts/DefaultLayout.vue";
import { useBookingStore } from "../stores/booking";

const route = useRoute();
const router = useRouter();
const bookingStore = useBookingStore();

const showInfo = ref({});
const performances = ref([]);
const selectedPerformance = ref(null);
const loading = ref(true);

// Group performances by date
const groupedPerformances = computed(() => {
	const groups = {};
	performances.value.forEach((perf) => {
		const date = new Date(perf.datetime).toDateString();
		if (!groups[date]) {
			groups[date] = [];
		}
		groups[date].push(perf);
	});
	return groups;
});

// Methods
const formatDate = (dateString) => {
	const date = new Date(dateString);
	const days = [
		"Chủ Nhật",
		"Thứ 2",
		"Thứ 3",
		"Thứ 4",
		"Thứ 5",
		"Thứ 6",
		"Thứ 7",
	];
	return `${days[date.getDay()]}, ${date.getDate()}/${
		date.getMonth() + 1
	}/${date.getFullYear()}`;
};

const formatTime = (datetime) => {
	const date = new Date(datetime);
	return date.toLocaleTimeString("vi-VN", {
		hour: "2-digit",
		minute: "2-digit",
	});
};

const selectPerformance = (performance) => {
	if (performance.available_seats > 0) {
		selectedPerformance.value = performance;
		bookingStore.selectedPerformance = performance;
	}
};

const continueToSeatSelection = () => {
	if (selectedPerformance.value) {
		const performanceData = {
			...selectedPerformance.value,
			service_fee_per_ticket: showInfo.value.service_fee_per_ticket || 0,
			show_name: showInfo.value.name,
		};

		sessionStorage.setItem(
			"selectedPerformance",
			JSON.stringify(performanceData)
		);

		router.push(`/booking/${route.params.showId}/seats`);
	}
};

onMounted(async () => {
	try {
		// Initialize session
		bookingStore.initSession();

		// Load show details
		await bookingStore.loadShowDetail(route.params.showId);
		showInfo.value = bookingStore.currentShow;
		performances.value = bookingStore.performances;
	} catch (error) {
		console.error("Failed to load show:", error);
	} finally {
		loading.value = false;
	}
});
</script>
