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
					<div class="bg-white rounded-lg shadow-lg p-6">
						<!-- Venue Info & Layout Image -->
						<div class="mb-6 text-center">
							<h2 class="text-xl font-bold mb-2">
								{{
									performanceInfo.show?.venue?.name ||
									"Nhà hát"
								}}
							</h2>
							<div class="mb-4">
								<img
									:src="venueLayoutImage"
									:alt="
										'Sơ đồ ' +
										(performanceInfo.show?.venue?.name ||
											'nhà hát')
									"
									class="mx-auto max-w-xs opacity-75 mb-2"
									v-if="venueLayoutImage"
								/>
								<p class="text-sm text-gray-500">
									Sơ đồ tham khảo - Màu sắc có thể khác với
									ghế thực tế
								</p>
							</div>
						</div>

						<!-- Stage -->
						<div class="mb-8 text-center">
							<div
								class="bg-gradient-to-r from-gray-700 to-gray-900 text-white py-4 rounded-t-2xl mx-auto shadow-lg"
								style="max-width: 600px"
							>
								<div class="text-lg font-bold">SÂN KHẤU</div>
								<div class="text-sm opacity-75">STAGE</div>
							</div>
						</div>

						<!-- Price Categories Legend -->
						<div class="mb-6 bg-gray-50 rounded-lg p-4">
							<h3 class="font-semibold mb-3">Phân loại vé:</h3>
							<div class="grid grid-cols-2 md:grid-cols-3 gap-3">
								<div
									v-for="(category, code) in priceCategories"
									:key="code"
									class="flex items-center space-x-2"
								>
									<div
										class="w-4 h-4 rounded border"
										:style="{
											backgroundColor: category.color,
										}"
									></div>
									<div class="text-sm">
										<div class="font-medium">
											{{ category.name }}
										</div>
										<div class="text-gray-600">
											{{ formatPrice(category.price) }}
										</div>
									</div>
								</div>
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
									<h3
										class="text-center font-semibold mb-4 text-lg"
									>
										{{ section.name }}
									</h3>

									<div
										class="flex flex-col items-center space-y-3"
									>
										<div
											v-for="row in section.rows"
											:key="row.label"
											class="flex items-center justify-center"
										>
											<!-- Row Label Left -->
											<span
												class="w-8 text-right mr-4 font-semibold text-gray-600"
											>
												{{ row.label }}
											</span>

											<!-- Seats with center alignment -->
											<div class="flex justify-center">
												<!-- Center-out layout -->
												<div
													v-if="
														row.seats.style ===
														'center_out'
													"
													class="flex gap-1 items-center"
												>
													<!-- Left side (odd numbers) -->
													<button
														v-for="seat in row.seats
															.oddSeats"
														:key="seat.id"
														@click="
															toggleSeat(seat)
														"
														:disabled="
															seat.status !==
																'available' &&
															!isSelected(seat)
														"
														:class="[
															'w-8 h-8 text-xs font-bold rounded border transition-colors',
															getSeatClass(seat),
														]"
														:style="
															getSeatStyle(seat)
														"
													>
														{{ seat.number }}
													</button>

													<!-- Center aisle -->
													<div class="w-8"></div>

													<!-- Right side (even numbers) -->
													<button
														v-for="seat in row.seats
															.evenSeats"
														:key="seat.id"
														@click="
															toggleSeat(seat)
														"
														:disabled="
															seat.status !==
																'available' &&
															!isSelected(seat)
														"
														:class="[
															'w-8 h-8 text-xs font-bold rounded border transition-colors',
															getSeatClass(seat),
														]"
														:style="
															getSeatStyle(seat)
														"
													>
														{{ seat.number }}
													</button>
												</div>

												<!-- Linear layout (left-to-right, vertical) -->
												<div
													v-else
													class="flex gap-1 items-center"
												>
													<button
														v-for="seat in row.seats
															.seats"
														:key="seat.id"
														@click="
															toggleSeat(seat)
														"
														:disabled="
															seat.status !==
																'available' &&
															!isSelected(seat)
														"
														:class="[
															'w-8 h-8 text-xs font-bold rounded border transition-colors',
															getSeatClass(seat),
														]"
														:style="
															getSeatStyle(seat)
														"
													>
														{{ seat.number }}
													</button>
												</div>
											</div>
											<!-- Row Label Right -->
											<span
												class="w-8 text-left ml-4 font-semibold text-gray-600"
											>
												{{ row.label }}
											</span>
										</div>
									</div>
								</div>
							</div>
						</div>

						<!-- Status Legend -->
						<div class="mt-6 bg-white rounded-lg shadow p-4">
							<h4 class="font-semibold mb-3">Trạng thái ghế:</h4>
							<div class="flex flex-wrap gap-6 justify-center">
								<div class="flex items-center space-x-2">
									<div
										class="w-5 h-5 bg-green-500 rounded border"
									></div>
									<span class="text-sm">Còn trống</span>
								</div>
								<div class="flex items-center space-x-2">
									<div
										class="w-5 h-5 bg-yellow-500 rounded border"
									></div>
									<span class="text-sm">Đang chọn</span>
								</div>
								<div class="flex items-center space-x-2">
									<div
										class="w-5 h-5 bg-red-500 rounded border"
									></div>
									<span class="text-sm">Đã bán</span>
								</div>
								<div class="flex items-center space-x-2">
									<div
										class="w-5 h-5 bg-gray-400 rounded border"
									></div>
									<span class="text-sm">Đang giữ</span>
								</div>
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
									<span>
										{{ seat.section_name }} - {{ seat.row
										}}{{ seat.number }}
									</span>
									<span class="font-semibold">
										{{ formatPrice(seat.price) }}
									</span>
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
				numbering_style: seat.numbering_style,
			};
		}

		sections[seat.section_id].rows[seat.row].seats.push(seat);
	});

	// Convert to array and sort
	return Object.values(sections).map((section) => ({
		...section,
		rows: Object.values(section.rows)
			.map((row) => ({
				...row,
				seats: sortSeatsForDisplay(row.seats, row.numbering_style),
			}))
			.sort((a, b) => {
				// Custom sort cho rows
				const order = [
					"A",
					"B",
					"C",
					"D",
					"E",
					"F",
					"G",
					"H",
					"I",
					"J",
					"K",
					"L",
					"M",
					"N",
					"O",
					"P",
					"Q",
					"R",
					"S",
					"T",
					"U",
					"V",
					"W",
					"X",
					"Y",
					"Z",
					"AA",
					"BB",
					"CC",
				];
				return order.indexOf(a.label) - order.indexOf(b.label);
			}),
	}));
});

const sortSeatsForDisplay = (seats, numberingStyle) => {
	// 🔧 FIX: Chỉ render seats có trong API response (skip gaps)
	const seatNumbers = new Set(seats.map((s) => s.number));

	if (numberingStyle === "center_out") {
		// Chỉ lấy seats thực sự có trong API
		const oddSeats = seats
			.filter((s) => s.number % 2 === 1)
			.sort((a, b) => b.number - a.number);
		const evenSeats = seats
			.filter((s) => s.number % 2 === 0)
			.sort((a, b) => a.number - b.number);

		return { oddSeats, evenSeats, style: "center_out" };
	} else {
		return {
			seats: seats.sort((a, b) => a.number - b.number),
			style: "linear",
		};
	}
};
// Thêm computed cho numbering info
const numberingInfo = computed(() => {
	return seatMap.value?.numbering_info || {};
});

const priceCategories = computed(() => {
	return seatMap.value?.price_categories || {};
});

const venueLayoutImage = computed(() => {
	const venueType = performanceInfo.value.show?.venue?.venue_type;
	if (venueType === "opera") {
		return "/images/ho-guom-opera-layout.jpg";
	}
	return null;
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
	const baseClasses = "w-8 h-8 text-xs rounded transition-all border";

	if (isSelected(seat)) {
		return `${baseClasses} bg-yellow-500 hover:bg-yellow-600 text-white border-yellow-400`;
	}

	switch (seat.status) {
		case "available":
			return `${baseClasses} text-white border-gray-300 hover:opacity-80 cursor-pointer`;
		case "sold":
			return `${baseClasses} bg-red-500 text-white cursor-not-allowed border-red-400`;
		case "reserved":
			return `${baseClasses} bg-gray-400 text-white cursor-not-allowed border-gray-300`;
		default:
			return `${baseClasses} bg-gray-300 cursor-not-allowed border-gray-200`;
	}
};

const getSeatStyle = (seat) => {
	if (seat.status === "available" && !isSelected(seat)) {
		const color = seat.price_category_color || "#10B981";
		return {
			backgroundColor: color,
			borderColor: color,
		};
	}
	return {};
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
		console.log("Seat map data:", response.data); // Debug
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
