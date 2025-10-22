<template>
	<DefaultLayout>
		<div class="container mx-auto px-4 py-8">
			<nav class="mb-8">
				<ol class="flex items-center space-x-2 uppercase text-sm">
					<li>
						<router-link
							to="/"
							class="uppercase text-[#d8a669] hover:text-[#b8884d] font-medium transition"
						>
							Trang chủ
						</router-link>
					</li>
					<li class="uppercase text-[#a0866b]">/</li>
					<li class="uppercase text-[#372e2d] font-semibold">
						Chọn suất diễn
					</li>
				</ol>
			</nav>

			<div v-if="loading" class="flex justify-center py-12">
				<DuongCamLoading size="lg" message="Đang tải suất diễn..." />
			</div>

			<template v-else>
				<div
					class="bg-[#fdfcf0] border border-[#d8a669]/30 rounded-lg shadow-lg p-6 md:p-8 mb-8"
				>
					<div class="grid md:grid-cols-3 gap-6 md:gap-8">
						<div class="md:col-span-1">
							<div
								class="relative w-full poster-container bg-[#e8dcc8] rounded-lg overflow-hidden border-2 border-[#d8a669]/20 group cursor-pointer shadow-md hover:shadow-xl transition-shadow duration-300 mx-auto"
								@click="openTrailer"
							>
								<img
									v-if="showInfo.poster"
									:src="showInfo.poster"
									:alt="showInfo.name"
									class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
								/>
								<div
									v-else
									class="w-full h-full bg-gradient-to-br from-[#d8a669]/20 to-[#372e2d]/20 flex items-center justify-center"
								>
									<svg
										class="w-16 md:w-24 h-16 md:h-24 uppercase text-[#d8a669]/30"
										fill="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											d="M4 4h16v12H4V4m0 14h16v2H4v-2z"
										/>
									</svg>
								</div>

								<div
									v-if="showInfo.trailer_url"
									class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-all duration-300 flex items-center justify-center"
								>
									<div
										class="uppercase text-center transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300"
									>
										<div
											class="w-16 h-16 md:w-20 md:h-20 bg-white/95 rounded-full flex items-center justify-center mb-2 md:mb-3 mx-auto shadow-2xl"
										>
											<svg
												class="w-8 h-8 md:w-10 md:h-10 uppercase text-[#d8a669] ml-1"
												fill="currentColor"
												viewBox="0 0 24 24"
											>
												<path d="M8 5v14l11-7z" />
											</svg>
										</div>
										<p
											class="text-white font-bold text-base md:text-lg drop-shadow-lg"
										>
											Xem Trailer
										</p>
									</div>
								</div>
							</div>
						</div>

						<div class="md:col-span-2 space-y-4">
							<h1
								class="uppercase text-2xl md:text-3xl lg:text-4xl font-bold text-[#372e2d]"
							>
								{{ showInfo.name }}
							</h1>

							<div class="flex flex-wrap gap-3">
								<button
									v-if="showInfo.trailer_url"
									@click="openTrailer"
									class="flex items-center gap-2 bg-white border-2 border-[#d8a669] uppercase text-[#d8a669] px-4 md:px-6 py-2.5 md:py-3 rounded-lg font-medium hover:bg-[#d8a669] hover:text-white transition-all duration-200 shadow-md hover:shadow-xl transform hover:scale-105 active:scale-95"
								>
									<svg
										class="w-4 h-4 md:w-5 md:h-5"
										fill="currentColor"
										viewBox="0 0 24 24"
									>
										<path d="M8 5v14l11-7z" />
									</svg>
									<span class="uppercase text-sm md:text-base"
										>Xem Trailer</span
									>
								</button>

								<button
									@click="scrollToPerformances"
									class="flex items-center gap-2 bg-[#d8a669] uppercase text-white px-4 md:px-6 py-2.5 md:py-3 rounded-lg font-bold hover:bg-[#b8884d] transition-all duration-200 shadow-md hover:shadow-xl transform hover:scale-105 active:scale-95"
								>
									<svg
										class="w-4 h-4 md:w-5 md:h-5"
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
									<span class="uppercase text-sm md:text-base"
										>Đặt vé ngay</span
									>
								</button>
							</div>

							<div
								class="space-y-2 text-[#372e2d] text-sm md:text-base pt-2"
							>
								<p class="font-medium flex items-center gap-2">
									<span class="uppercase text-[#d8a669]"
										>🎭</span
									>
									<span class="uppercase text-gray-600"
										>Thể loại:</span
									>
									<span class="uppercase font-semibold">{{
										showInfo.category
									}}</span>
								</p>
								<p class="font-medium flex items-center gap-2">
									<span class="uppercase text-[#d8a669]"
										>⏱️</span
									>
									<span class="uppercase text-gray-600"
										>Thời lượng:</span
									>
									<span class="uppercase font-semibold"
										>{{
											showInfo.duration_minutes
										}}
										phút</span
									>
								</p>
								<p class="font-medium flex items-center gap-2">
									<span class="uppercase text-[#d8a669]"
										>📍</span
									>
									<span class="uppercase text-gray-600"
										>Địa điểm:</span
									>
									<span class="uppercase font-semibold">{{
										showInfo.venue?.name
									}}</span>
								</p>
							</div>

							<div class="relative">
								<div
									:class="[
										'prose max-w-none text-sm md:text-base',
										!showFullDescription &&
											'line-clamp-3 md:line-clamp-none',
									]"
								>
									<p class="text-[#372e2d] leading-relaxed">
										{{ showInfo.description }}
									</p>
								</div>

								<div
									v-if="
										!showFullDescription &&
										showInfo.description &&
										showInfo.description.length > 150
									"
									class="absolute bottom-0 left-0 right-0 h-8 bg-gradient-to-t from-[#fdfcf0] to-transparent pointer-events-none md:hidden"
								></div>

								<button
									v-if="
										showInfo.description &&
										showInfo.description.length > 150
									"
									@click="
										showFullDescription =
											!showFullDescription
									"
									class="mt-2 text-[#d8a669] font-medium hover:text-[#b8884d] transition flex items-center gap-1 text-sm md:hidden"
								>
									{{
										showFullDescription
											? "Thu gọn"
											: "Xem thêm"
									}}
									<svg
										class="w-4 h-4 transition-transform duration-200"
										:class="{
											'rotate-180': showFullDescription,
										}"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M19 9l-7 7-7-7"
										/>
									</svg>
								</button>
							</div>
						</div>
					</div>
				</div>

				<div
					v-if="showInfo.description_markdown"
					class="bg-[#fdfcf0] border border-[#d8a669]/30 rounded-lg shadow-lg p-6 md:p-8 mb-8"
				>
					<h2
						class="uppercase text-xl md:text-2xl font-bold mb-4 text-[#372e2d] flex items-center gap-2"
					>
						<svg
							class="w-5 h-5 md:w-6 md:h-6 uppercase text-[#d8a669]"
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
						Thông tin chi tiết
					</h2>

					<MarkdownCollapse
						:content="showInfo.description_markdown"
						:initialLines="3"
					/>
				</div>

				<div
					ref="performancesSection"
					id="performances"
					class="bg-[#fdfcf0] border border-[#d8a669]/30 rounded-lg shadow-lg p-6 md:p-8"
					style="scroll-margin-top: 80px"
				>
					<h2
						class="uppercase text-xl md:text-2xl font-bold mb-6 text-[#372e2d]"
					>
						Chọn suất diễn
					</h2>

					<div
						v-if="performances.length === 0"
						class="uppercase text-center text-[#372e2d] py-8"
					>
						Không có suất diễn nào
					</div>

					<div v-else class="space-y-6">
						<div
							v-for="(dateGroup, date) in groupedPerformances"
							:key="date"
						>
							<h3
								class="font-semibold uppercase text-base md:text-lg mb-4 text-[#372e2d] flex items-center"
							>
								{{ formatDate(date) }}
							</h3>

							<div
								class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-4"
							>
								<div
									v-for="performance in dateGroup"
									:key="performance.id"
									@click="selectPerformance(performance)"
									:class="[
										'relative border-2 rounded-xl p-3 md:p-4 uppercase text-center cursor-pointer transition-all duration-300',
										{
											'border-[#d8a669] bg-white hover:border-[#b8884d] hover:shadow-lg hover:bg-[#fdfcf0]':
												selectedPerformance?.id !==
													performance.id &&
												performance.available_seats > 0,
											'border-[#d8a669] bg-gradient-to-br from-[#d8a669] to-[#b8884d] shadow-2xl ring-4 ring-[#d8a669]/50 scale-105 -translate-y-1':
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
										v-if="
											selectedPerformance?.id ===
											performance.id
										"
										class="absolute -top-3 -right-3 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-lg border-2 border-[#d8a669] z-10"
									>
										<svg
											class="w-5 h-5 text-[#d8a669]"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="3"
												d="M5 13l4 4L19 7"
											/>
										</svg>
									</div>

									<div
										:class="[
											'uppercase text-base md:text-lg font-bold transition-colors duration-300',
											{
												'text-[#372e2d]':
													selectedPerformance?.id !==
													performance.id,
												'text-white':
													selectedPerformance?.id ===
													performance.id,
											},
										]"
									>
										{{ formatTime(performance.datetime) }}
									</div>
									<div
										:class="[
											'uppercase text-xs md:text-sm mt-2 font-medium transition-colors duration-300',
											{
												'uppercase text-[#372e2d]':
													performance.available_seats >
														0 &&
													selectedPerformance?.id !==
														performance.id,
												'text-white/90':
													performance.available_seats >
														0 &&
													selectedPerformance?.id ===
														performance.id,
												'uppercase text-red-600':
													performance.available_seats ===
													0,
											},
										]"
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

					<div
						v-if="selectedPerformance"
						class="mt-6 md:mt-8 flex justify-end"
					>
						<button
							@click="continueToSeatSelection"
							class="w-full md:w-auto bg-[#d8a669] uppercase text-white px-6 md:px-8 py-3 rounded-lg font-bold text-base md:text-lg shadow-lg hover:bg-[#b8884d] hover:shadow-xl transform hover:scale-105 active:scale-95 transition-all duration-200"
						>
							Tiếp tục chọn ghế →
						</button>
					</div>
				</div>
			</template>
		</div>

		<TrailerPopup
			:show="showTrailerPopup"
			:trailerUrl="showInfo.trailer_url"
			@close="closeTrailer"
		/>
	</DefaultLayout>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import DefaultLayout from "../layouts/DefaultLayout.vue";
import TrailerPopup from "../components/TrailerPopup.vue";
import MarkdownCollapse from "../components/MarkdownCollapse.vue";
import { useBookingStore } from "../stores/booking";
import DuongCamLoading from "@/components/common/DuongCamLoading.vue";
import { useToast } from "vue-toastification";

const route = useRoute();
const router = useRouter();
const bookingStore = useBookingStore();
const toast = useToast();

const showInfo = ref({});
const performances = ref([]);
const selectedPerformance = ref(null);
const loading = ref(true);

// Trailer popup state
const showTrailerPopup = ref(false);

// Description collapse state
const showFullDescription = ref(false);

// Ref to performances section
const performancesSection = ref(null);

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

const openTrailer = () => {
	if (showInfo.value.trailer_url) {
		showTrailerPopup.value = true;
		document.body.style.overflow = "hidden";
	}
};

const closeTrailer = () => {
	showTrailerPopup.value = false;
	document.body.style.overflow = "";
};

// [CẬP NHẬT] Scroll to performances section bằng JS
const scrollToPerformances = () => {
	if (performancesSection.value) {
		// Lấy chiều cao của header (nếu có)
		// Thay 'app-header-id' bằng ID thật của header nếu có,
		// hoặc ước lượng chiều cao (vd: 80px)
		const headerElement = document.getElementById("app-header"); // <-- THAY ID HEADER Ở ĐÂY (NẾU CÓ)
		const headerHeight = headerElement ? headerElement.offsetHeight : 80; // Ước lượng 80px

		const elementPosition = performancesSection.value.offsetTop;
		const offsetPosition = elementPosition - headerHeight;

		window.scrollTo({
			top: offsetPosition,
			behavior: "smooth",
		});
	}
};

onMounted(async () => {
	loading.value = true;
	try {
		bookingStore.initSession();
		await bookingStore.loadShowDetail(route.params.showId);
		showInfo.value = bookingStore.currentShow;
		performances.value = bookingStore.performances;
	} catch (error) {
		console.error("Failed to load show:", error);
		toast.error("Không thể tải chi tiết chương trình.");
	} finally {
		loading.value = false;

		// [CẬP NHẬT] Gọi scrollToPerformances bằng JS thay vì dựa vào scroll-mt
		if (route.hash === "#performances") {
			// Đợi DOM render xong mới scroll
			await nextTick();
			// Thêm delay nhỏ để đảm bảo mọi thứ (vd: ảnh) đã load xong chiều cao
			setTimeout(() => {
				scrollToPerformances();
			}, 100);
		}
	}
});
</script>

<style scoped>
/* Poster responsive sizing */
.poster-container {
	aspect-ratio: 2/3;
	max-width: 280px; /* Mobile: smaller */
}

@media (min-width: 768px) {
	.poster-container {
		aspect-ratio: 2/3;
		max-width: 100%; /* Desktop: full width of column */
	}
}

/* Line clamp utility - chỉ mobile */
.line-clamp-3 {
	display: -webkit-box;
	-webkit-line-clamp: 3;
	-webkit-box-orient: vertical;
	overflow: hidden;
}

/* Desktop: no line clamp */
@media (min-width: 768px) {
	.md\:line-clamp-none {
		display: block;
		-webkit-line-clamp: unset;
		-webkit-box-orient: unset;
	}
}
</style>
