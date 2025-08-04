<template>
	<DefaultLayout>
		<div class="container mx-auto px-4 py-8">
			<!-- Breadcrumb -->
			<nav class="mb-6">
				<ol class="flex items-center space-x-2 text-sm">
					<li>
						<router-link
							to="/"
							class="text-gray-500 hover:text-primary-600"
						>
							Trang chủ
						</router-link>
					</li>
					<li class="text-gray-400">/</li>
					<li>
						<router-link
							:to="`/booking/${$route.params.showId}`"
							class="text-gray-500 hover:text-primary-600"
						>
							Chọn suất diễn
						</router-link>
					</li>
					<li class="text-gray-400">/</li>
					<li class="text-gray-700 font-medium">Chọn ghế</li>
				</ol>
			</nav>

			<!-- Loading -->
			<div v-if="loading" class="flex justify-center py-12">
				<div
					class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"
				></div>
			</div>

			<div v-else class="grid grid-cols-1 lg:grid-cols-4 gap-6">
				<!-- Seat Map - 3 columns -->
				<div class="lg:col-span-3">
					<div class="bg-white rounded-lg shadow-lg p-4">
						<!-- Stage -->
						<div class="mb-8 text-center">
							<div
								class="bg-gray-800 text-white py-4 rounded-t-3xl mx-auto"
								style="max-width: 600px"
							>
								SÂN KHẤU
							</div>
						</div>

						<!-- Seat Grid -->
						<div class="overflow-auto pb-4">
							<div class="min-w-max px-4">
								<!-- Render seats from backend data -->
								<div
									v-for="section in seatsBySections"
									:key="section.id"
									class="mb-8"
								>
									<h3 class="text-center font-semibold mb-4">
										{{ section.name }}
									</h3>

									<div
										v-for="row in section.rows"
										:key="row.label"
										class="flex items-center mb-2"
									>
										<span
											class="w-8 text-right mr-4 font-semibold"
											>{{ row.label }}</span
										>

										<div class="flex gap-1">
											<button
												v-for="seat in row.seats"
												:key="seat.id"
												@click="toggleSeat(seat)"
												:disabled="
													seat.status !==
														'available' &&
													!isSelected(seat)
												"
												:class="[
													'w-8 h-8 text-xs rounded transition-all',
													getSeatClass(seat),
												]"
												:title="`${
													section.name
												} - Hàng ${row.label} Ghế ${
													seat.number
												} - ${formatPrice(seat.price)}`"
											>
												{{ seat.number }}
											</button>
										</div>

										<span
											class="w-8 text-left ml-4 font-semibold"
											>{{ row.label }}</span
										>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Legend -->
					<div class="mt-4 bg-white rounded-lg shadow p-4">
						<div class="flex flex-wrap gap-6 justify-center">
							<div class="flex items-center space-x-2">
								<div class="w-5 h-5 bg-green-500 rounded"></div>
								<span class="text-sm">Còn trống</span>
							</div>
							<div class="flex items-center space-x-2">
								<div
									class="w-5 h-5 bg-yellow-500 rounded"
								></div>
								<span class="text-sm">Đang chọn</span>
							</div>
							<div class="flex items-center space-x-2">
								<div class="w-5 h-5 bg-red-500 rounded"></div>
								<span class="text-sm">Đã bán</span>
							</div>
							<div class="flex items-center space-x-2">
								<div class="w-5 h-5 bg-gray-400 rounded"></div>
								<span class="text-sm">Đang giữ</span>
							</div>
						</div>
					</div>
				</div>

				<!-- Booking Summary - 1 column -->
				<div class="lg:col-span-1">
					<div class="bg-white rounded-lg shadow-lg p-6 sticky top-4">
						<h3 class="text-lg font-bold mb-4">Thông tin đặt vé</h3>

						<!-- Show Info -->
						<div class="mb-4 pb-4 border-b">
							<h4 class="font-semibold">
								{{ performanceInfo.show_name }}
							</h4>
							<p class="text-sm text-gray-600">
								{{ formatDate(performanceInfo.datetime) }}
							</p>
							<p class="text-sm text-gray-600">
								Suất: {{ formatTime(performanceInfo.datetime) }}
							</p>
						</div>

						<!-- Selected Seats -->
						<div class="mb-4 pb-4 border-b">
							<h4 class="font-semibold mb-2">Ghế đã chọn:</h4>
							<div
								v-if="selectedSeats.length === 0"
								class="text-sm text-gray-500"
							>
								Chưa chọn ghế nào
							</div>
							<div
								v-else
								class="space-y-2 max-h-40 overflow-y-auto"
							>
								<div
									v-for="seat in selectedSeats"
									:key="seat.id"
									class="flex justify-between items-center text-sm p-2 bg-gray-50 rounded"
								>
									<span
										>{{ seat.section_name }} - {{ seat.row
										}}{{ seat.number }}</span
									>
									<span class="font-semibold">{{
										formatPrice(seat.price)
									}}</span>
								</div>
							</div>
						</div>

						<!-- Total -->
						<div class="mb-6">
							<div class="flex justify-between items-center">
								<span class="font-semibold">Tổng cộng:</span>
								<span
									class="text-xl font-bold text-primary-600"
								>
									{{ formatPrice(totalAmount) }}
								</span>
							</div>
						</div>

						<!-- Timer -->
						<div
							v-if="selectedSeats.length > 0 && reservationExpiry"
							class="mb-4 p-3 bg-yellow-50 rounded-lg"
						>
							<div class="text-sm text-yellow-800">
								⏱️ Thời gian giữ ghế:
								<span class="font-bold">{{
									timeLeftFormatted
								}}</span>
							</div>
						</div>

						<!-- Continue Button -->
						<button
							:disabled="selectedSeats.length === 0"
							@click="continueToCustomerInfo"
							:class="[
								'w-full py-3 rounded-lg font-semibold transition',
								selectedSeats.length > 0
									? 'bg-primary-600 text-white hover:bg-primary-700'
									: 'bg-gray-300 text-gray-500 cursor-not-allowed',
							]"
						>
							Tiếp tục
						</button>
					</div>
				</div>
			</div>
		</div>
	</DefaultLayout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import DefaultLayout from "../layouts/DefaultLayout.vue";
import { useBookingStore } from "../stores/booking";
import { bookingAPI } from "../api/booking";

const router = useRouter();
const route = useRoute();
const bookingStore = useBookingStore();

// State
const loading = ref(true);
const seatMap = ref(null);
const selectedSeats = ref([]);
const performanceInfo = ref({});
const reservationExpiry = ref(null);
const timeLeft = ref(0);
let timer = null;

// Computed
const seatsBySections = computed(() => {
	if (!seatMap.value) return [];

	const sections = {};

	seatMap.value.seats.forEach((seat) => {
		if (!sections[seat.section_id]) {
			sections[seat.section_id] = {
				id: seat.section_id,
				name: seat.section_name,
				rows: {},
			};
		}

		if (!sections[seat.section_id].rows[seat.row]) {
			sections[seat.section_id].rows[seat.row] = {
				label: seat.row,
				seats: [],
			};
		}

		sections[seat.section_id].rows[seat.row].seats.push(seat);
	});

	// Convert to array and sort
	return Object.values(sections).map((section) => ({
		...section,
		rows: Object.values(section.rows).sort((a, b) =>
			a.label.localeCompare(b.label)
		),
	}));
});

const totalAmount = computed(() => {
	return selectedSeats.value.reduce((sum, seat) => sum + seat.price, 0);
});

const timeLeftFormatted = computed(() => {
	const mins = Math.floor(timeLeft.value / 60);
	const secs = timeLeft.value % 60;
	return `${mins}:${secs.toString().padStart(2, "0")}`;
});

// Methods
const formatPrice = (price) => {
	return new Intl.NumberFormat("vi-VN", {
		style: "currency",
		currency: "VND",
	}).format(price || 0);
};

const formatDate = (datetime) => {
	const date = new Date(datetime);
	return date.toLocaleDateString("vi-VN");
};

const formatTime = (datetime) => {
	const date = new Date(datetime);
	return date.toLocaleTimeString("vi-VN", {
		hour: "2-digit",
		minute: "2-digit",
	});
};

const getSeatClass = (seat) => {
	if (isSelected(seat)) {
		return "bg-yellow-500 hover:bg-yellow-600 text-white";
	}

	switch (seat.status) {
		case "available":
			return "bg-green-500 hover:bg-green-600 text-white";
		case "sold":
			return "bg-red-500 text-white cursor-not-allowed";
		case "reserved":
			return "bg-gray-400 text-white cursor-not-allowed";
		default:
			return "bg-gray-300 cursor-not-allowed";
	}
};

const isSelected = (seat) => {
	return selectedSeats.value.some((s) => s.id === seat.id);
};

const toggleSeat = async (seat) => {
	if (seat.status !== "available" && !isSelected(seat)) return;

	const index = selectedSeats.value.findIndex((s) => s.id === seat.id);

	if (index > -1) {
		// Deselect
		selectedSeats.value.splice(index, 1);

		// Release seat
		try {
			await bookingAPI.releaseSeats([seat.id], bookingStore.sessionId);
		} catch (error) {
			console.error("Failed to release seat:", error);
		}
	} else {
		// Check max seats
		if (selectedSeats.value.length >= 8) {
			alert("Bạn chỉ có thể chọn tối đa 8 ghế");
			return;
		}

		// Reserve seat
		try {
			const response = await bookingAPI.reserveSeats(
				performanceInfo.value.id,
				[...selectedSeats.value.map((s) => s.id), seat.id],
				bookingStore.sessionId
			);

			selectedSeats.value = response.data.seats;
			reservationExpiry.value = new Date(response.data.expires_at);

			// Start/restart timer
			startTimer();
		} catch (error) {
			alert("Không thể giữ ghế này");
		}
	}
};

const startTimer = () => {
	if (timer) clearInterval(timer);

	timer = setInterval(() => {
		if (reservationExpiry.value) {
			const now = new Date();
			const diff = Math.floor((reservationExpiry.value - now) / 1000);
			timeLeft.value = Math.max(0, diff);

			if (timeLeft.value === 0) {
				clearInterval(timer);
				alert("Hết thời gian giữ ghế. Vui lòng chọn lại.");
				selectedSeats.value = [];
				loadSeatMap();
			}
		}
	}, 1000);
};

const continueToCustomerInfo = () => {
	if (selectedSeats.value.length > 0) {
		bookingStore.selectedSeats = selectedSeats.value;
		sessionStorage.setItem(
			"selectedSeats",
			JSON.stringify(selectedSeats.value)
		);
		router.push(`/booking/${route.params.showId}/customer-info`);
	}
};

const loadSeatMap = async () => {
	try {
		const response = await bookingAPI.getSeatMap(performanceInfo.value.id);
		seatMap.value = response.data;
	} catch (error) {
		console.error("Failed to load seat map:", error);
	}
};

onMounted(async () => {
	try {
		// Get performance info from session
		const savedPerformance = sessionStorage.getItem("selectedPerformance");
		if (savedPerformance) {
			performanceInfo.value = JSON.parse(savedPerformance);
		} else {
			router.push(`/booking/${route.params.showId}`);
			return;
		}

		// Load seat map
		await loadSeatMap();
	} catch (error) {
		console.error("Failed to load:", error);
	} finally {
		loading.value = false;
	}
});

onUnmounted(() => {
	if (timer) {
		clearInterval(timer);
	}
});
</script>
