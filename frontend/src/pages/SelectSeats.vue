<template>
	<DefaultLayout>
		<div class="min-h-screen bg-gray-50 py-8">
			<div class="container mx-auto px-4">
				<!-- Loading State -->
				<div
					v-if="loading"
					class="flex justify-center items-center min-h-[400px]"
				>
					<div class="text-center">
						<div
							class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"
						></div>
						<p class="text-gray-600">Đang tải sơ đồ ghế...</p>
					</div>
				</div>

				<!-- Main Content -->
				<div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
					<!-- Seat Map - 2 columns -->
					<div class="lg:col-span-2">
						<div class="bg-white rounded-lg shadow-lg p-6">
							<!-- Performance Info Header -->
							<div class="mb-6 text-center border-b pb-4">
								<h2
									class="text-2xl font-bold mb-2 text-gray-800"
								>
									{{ showInfo.name }}
								</h2>
								<div
									class="flex items-center justify-center gap-4 text-gray-600 text-sm"
								>
									<div class="flex items-center gap-1">
										<svg
											class="w-4 h-4"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
											/>
										</svg>
										<span>{{
											performanceData.day_of_week
										}}</span>
									</div>
									<div class="flex items-center gap-1">
										<svg
											class="w-4 h-4"
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
										<span
											>{{ performanceData.date }} -
											{{ performanceData.time }}</span
										>
									</div>
								</div>
								<p class="text-sm text-gray-500 mt-2">
									{{ venueInfo.name }}
								</p>
							</div>

							<!-- Stage -->
							<div class="mb-8">
								<div
									class="bg-gradient-to-b from-gray-800 to-gray-900 text-white py-4 px-8 rounded-t-lg text-center mx-auto max-w-md shadow-lg"
								>
									<div class="text-lg font-bold">
										SÂN KHẤU
									</div>
									<div class="text-sm opacity-75">STAGE</div>
								</div>
							</div>

							<!-- Price Categories Legend -->
							<div
								class="mb-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 border border-blue-100"
							>
								<h3 class="font-semibold mb-3 text-gray-700">
									📋 Phân loại vé:
								</h3>
								<div
									class="grid grid-cols-2 md:grid-cols-3 gap-3"
								>
									<div
										v-for="(
											category, code
										) in priceCategories"
										:key="code"
										class="flex items-center space-x-2 bg-white rounded-lg p-2 shadow-sm"
									>
										<div
											class="w-5 h-5 rounded border-2 border-gray-300"
											:style="{
												backgroundColor: category.color,
											}"
										></div>
										<div class="text-sm">
											<div
												class="font-medium text-gray-800"
											>
												{{ category.name }}
											</div>
											<div
												class="text-primary-600 font-semibold"
											>
												{{
													formatPrice(category.price)
												}}
											</div>
										</div>
									</div>
								</div>
							</div>

							<!-- Seat Grid -->
							<div class="overflow-auto pb-4">
								<div class="min-w-max px-4">
									<div
										v-for="section in seatsBySections"
										:key="section.id"
										class="mb-8"
									>
										<h3
											class="text-center font-semibold mb-4 text-lg text-gray-700"
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
													class="w-10 text-right mr-4 font-bold text-gray-700 text-sm"
													>{{ row.label }}</span
												>

												<!-- Seats -->
												<div
													class="flex justify-center"
												>
													<!-- Center-out layout -->
													<div
														v-if="
															row.seats.style ===
															'center_out'
														"
														class="flex gap-1 items-center"
													>
														<!-- Left side (odd) -->
														<button
															v-for="seat in row
																.seats.oddSeats"
															:key="seat.id"
															@click="
																toggleSeat(seat)
															"
															:disabled="
																seat.status !==
																	'available' &&
																!isSelected(
																	seat
																)
															"
															:class="[
																'w-9 h-9 text-xs font-bold rounded-lg border-2 transition-all duration-200',
																getSeatClass(
																	seat
																),
															]"
															:style="{
																backgroundColor:
																	getSeatBackgroundColor(
																		seat
																	),
																borderColor:
																	getSeatBorderColor(
																		seat
																	),
																marginRight:
																	seat.spacing_after
																		? `${seat.spacing_after}px`
																		: '2px',
															}"
															@mouseenter="
																showSeatTooltip(
																	seat,
																	$event
																)
															"
															@mouseleave="
																hideSeatTooltip
															"
														>
															{{
																seat.display_number
															}}
														</button>

														<!-- Center aisle -->
														<div class="w-10"></div>

														<!-- Right side (even) -->
														<button
															v-for="seat in row
																.seats
																.evenSeats"
															:key="seat.id"
															@click="
																toggleSeat(seat)
															"
															:disabled="
																seat.status !==
																	'available' &&
																!isSelected(
																	seat
																)
															"
															:class="[
																'w-9 h-9 text-xs font-bold rounded-lg border-2 transition-all duration-200',
																getSeatClass(
																	seat
																),
															]"
															:style="{
																backgroundColor:
																	getSeatBackgroundColor(
																		seat
																	),
																borderColor:
																	getSeatBorderColor(
																		seat
																	),
																marginRight:
																	seat.spacing_after
																		? `${seat.spacing_after}px`
																		: '2px',
															}"
															@mouseenter="
																showSeatTooltip(
																	seat,
																	$event
																)
															"
															@mouseleave="
																hideSeatTooltip
															"
														>
															{{
																seat.display_number
															}}
														</button>
													</div>

													<!-- Linear layout -->
													<div
														v-else
														class="flex gap-1 items-center"
													>
														<button
															v-for="seat in row
																.seats.seats"
															:key="seat.id"
															@click="
																toggleSeat(seat)
															"
															:disabled="
																seat.status !==
																	'available' &&
																!isSelected(
																	seat
																)
															"
															:class="[
																'w-9 h-9 text-xs font-bold rounded-lg border-2 transition-all duration-200',
																getSeatClass(
																	seat
																),
															]"
															:style="{
																backgroundColor:
																	getSeatBackgroundColor(
																		seat
																	),
																borderColor:
																	getSeatBorderColor(
																		seat
																	),
																marginRight:
																	seat.spacing_after
																		? `${seat.spacing_after}px`
																		: '2px',
															}"
															@mouseenter="
																showSeatTooltip(
																	seat,
																	$event
																)
															"
															@mouseleave="
																hideSeatTooltip
															"
														>
															{{
																seat.display_number
															}}
														</button>
													</div>
												</div>

												<!-- Row Label Right -->
												<span
													class="w-10 text-left ml-4 font-bold text-gray-700 text-sm"
													>{{ row.label }}</span
												>
											</div>
										</div>
									</div>
								</div>
							</div>

							<!-- Status Legend -->
							<div
								class="mt-6 bg-white rounded-lg shadow-md p-4 border border-gray-200"
							>
								<h4 class="font-semibold mb-3 text-gray-700">
									📌 Trạng thái ghế:
								</h4>
								<div
									class="flex flex-wrap gap-4 justify-center"
								>
									<div class="flex items-center space-x-2">
										<div
											class="w-6 h-6 bg-green-500 rounded-lg border-2 border-green-600"
										></div>
										<span class="text-sm text-gray-700"
											>Còn trống</span
										>
									</div>
									<div class="flex items-center space-x-2">
										<div
											class="w-6 h-6 bg-yellow-500 rounded-lg border-2 border-yellow-600"
										></div>
										<span class="text-sm text-gray-700"
											>Đang chọn</span
										>
									</div>
									<div class="flex items-center space-x-2">
										<div
											class="w-6 h-6 bg-red-500 rounded-lg border-2 border-red-600"
										></div>
										<span class="text-sm text-gray-700"
											>Đã bán</span
										>
									</div>
									<div class="flex items-center space-x-2">
										<div
											class="w-6 h-6 bg-gray-400 rounded-lg border-2 border-gray-500"
										></div>
										<span class="text-sm text-gray-700"
											>Đang giữ</span
										>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Booking Summary Sidebar - 1 column -->
					<div class="lg:col-span-1">
						<div
							class="bg-white rounded-lg shadow-lg p-6 sticky top-4"
						>
							<h3
								class="text-xl font-bold mb-4 text-gray-800 border-b pb-2"
							>
								🎫 Thông tin đặt vé
							</h3>

							<!-- Show Info -->
							<div class="mb-4 pb-4 border-b">
								<div class="flex items-start gap-3">
									<div
										class="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg flex items-center justify-center text-white font-bold text-xl flex-shrink-0"
									>
										🎭
									</div>
									<div class="flex-1">
										<h4
											class="font-bold text-gray-800 mb-1"
										>
											{{ showInfo.name }}
										</h4>
										<div
											class="space-y-1 text-sm text-gray-600"
										>
											<div
												class="flex items-center gap-2"
											>
												<svg
													class="w-4 h-4 text-primary-500"
													fill="none"
													stroke="currentColor"
													viewBox="0 0 24 24"
												>
													<path
														stroke-linecap="round"
														stroke-linejoin="round"
														stroke-width="2"
														d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
													/>
												</svg>
												<span class="font-medium"
													>{{
														performanceData.day_of_week
													}},
													{{
														performanceData.date
													}}</span
												>
											</div>
											<div
												class="flex items-center gap-2"
											>
												<svg
													class="w-4 h-4 text-primary-500"
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
												<span
													>Suất:
													<strong>{{
														performanceData.time
													}}</strong></span
												>
											</div>
											<div
												class="flex items-center gap-2"
											>
												<svg
													class="w-4 h-4 text-primary-500"
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
												<span class="text-xs">{{
													venueInfo.name
												}}</span>
											</div>
											<div
												v-if="showInfo.duration_minutes"
												class="flex items-center gap-2"
											>
												<svg
													class="w-4 h-4 text-primary-500"
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
												<span class="text-xs"
													>Thời lượng:
													{{
														showInfo.duration_minutes
													}}
													phút</span
												>
											</div>
										</div>
									</div>
								</div>

								<!-- Check-in Info -->
								<div
									v-if="venueInfo.checkin_minutes_before"
									class="mt-3 bg-amber-50 border border-amber-200 rounded-lg p-3"
								>
									<div
										class="flex items-center gap-2 text-amber-800 text-xs"
									>
										<svg
											class="w-4 h-4"
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
										<span
											>Vui lòng có mặt trước
											<strong
												>{{
													venueInfo.checkin_minutes_before
												}}
												phút</strong
											></span
										>
									</div>
								</div>
							</div>

							<!-- Layout Image Button -->
							<div
								v-if="venueInfo.layout_image_url"
								class="mb-4 pb-4 border-b"
							>
								<button
									@click="showLayoutModal = true"
									class="w-full py-2 px-4 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg font-semibold hover:from-blue-600 hover:to-purple-600 transition-all flex items-center justify-center gap-2"
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
											d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
										/>
									</svg>
									Xem sơ đồ nhà hát
								</button>
							</div>

							<!-- Selected Seats -->
							<div class="mb-4 pb-4 border-b">
								<h4
									class="font-semibold mb-2 text-gray-700 flex items-center justify-between"
								>
									<span>Ghế đã chọn</span>
									<span
										class="text-sm font-normal text-gray-500"
										>({{ selectedSeats.length }}/8)</span
									>
								</h4>
								<div
									v-if="selectedSeats.length === 0"
									class="text-sm text-gray-400 text-center py-6 bg-gray-50 rounded-lg"
								>
									<svg
										class="w-12 h-12 mx-auto mb-2 text-gray-300"
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
									<p>Chưa chọn ghế nào</p>
								</div>
								<div
									v-else
									class="space-y-2 max-h-56 overflow-y-auto pr-2"
								>
									<div
										v-for="seat in selectedSeats"
										:key="seat.id"
										class="flex justify-between items-center text-sm bg-gradient-to-r from-primary-50 to-purple-50 p-3 rounded-lg border border-primary-200"
									>
										<span class="font-bold text-gray-800">{{
											seat.full_label
										}}</span>
										<span
											class="text-primary-600 font-bold"
											>{{ formatPrice(seat.price) }}</span
										>
									</div>
								</div>
							</div>

							<!-- Total -->
							<div class="mb-4 pb-4 border-b">
								<div
									class="flex justify-between items-center bg-gradient-to-r from-primary-50 to-purple-50 p-4 rounded-lg"
								>
									<span
										class="font-bold text-gray-700 text-lg"
										>Tổng tiền:</span
									>
									<span
										class="text-2xl font-bold text-primary-600"
										>{{ formatPrice(totalAmount) }}</span
									>
								</div>
							</div>

							<!-- Timer -->
							<div
								v-if="timeLeft > 0"
								class="mb-4 p-4 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg border-2 border-yellow-300"
							>
								<div
									class="text-sm text-yellow-800 text-center"
								>
									<div class="font-semibold mb-1">
										⏱️ Thời gian giữ ghế
									</div>
									<div
										class="text-2xl font-bold text-orange-600"
									>
										{{ formatTime(timeLeft) }}
									</div>
								</div>
							</div>

							<!-- Continue Button -->
							<button
								@click="continueToCustomerInfo"
								:disabled="selectedSeats.length === 0"
								:class="[
									'w-full py-4 px-4 rounded-lg font-bold text-lg transition-all shadow-lg',
									selectedSeats.length > 0
										? 'bg-gradient-to-r from-green-500 to-green-600 text-white hover:from-green-600 hover:to-green-700 hover:shadow-xl transform hover:scale-105'
										: 'bg-gray-300 text-gray-500 cursor-not-allowed',
								]"
							>
								{{
									selectedSeats.length > 0
										? "✓ Tiếp tục"
										: "Vui lòng chọn ghế"
								}}
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Layout Image Modal -->
		<Teleport to="body">
			<div
				v-if="showLayoutModal"
				class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75 p-4"
				@click="showLayoutModal = false"
			>
				<div
					class="relative max-w-5xl w-full bg-white rounded-lg shadow-2xl"
					@click.stop
				>
					<button
						@click="showLayoutModal = false"
						class="absolute top-4 right-4 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors z-10"
					>
						<svg
							class="w-6 h-6 text-gray-700"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M6 18L18 6M6 6l12 12"
							/>
						</svg>
					</button>
					<div class="p-6">
						<h3 class="text-2xl font-bold mb-4 text-gray-800">
							Sơ đồ {{ venueInfo.name }}
						</h3>
						<img
							:src="venueInfo.layout_image_url"
							alt="Venue Layout"
							class="w-full rounded-lg shadow-lg"
						/>
					</div>
				</div>
			</div>
		</Teleport>

		<!-- Seat Tooltip with Image -->
		<Teleport to="body">
			<div
				v-if="tooltipVisible"
				:style="tooltipStyle"
				class="fixed z-50 bg-gradient-to-br from-gray-900 to-gray-800 text-white rounded-xl shadow-2xl pointer-events-none border-2 border-gray-700"
				style="min-width: 220px"
			>
				<!-- Seat Image -->
				<div
					v-if="tooltipData.seat_image_url"
					class="w-full h-32 rounded-t-lg overflow-hidden"
				>
					<img
						:src="tooltipData.seat_image_url"
						alt="Seat Image"
						class="w-full h-full object-cover"
					/>
				</div>

				<!-- Seat Info -->
				<div class="p-4">
					<div class="font-bold text-xl mb-2 text-yellow-300">
						{{ tooltipData.full_label }}
					</div>
					<div class="space-y-1 text-sm">
						<div class="flex items-center justify-between">
							<span class="text-gray-300">Giá:</span>
							<span class="font-bold text-green-400 text-lg">{{
								formatPrice(tooltipData.price)
							}}</span>
						</div>
						<div class="flex items-center justify-between">
							<span class="text-gray-300">Loại:</span>
							<span
								class="font-semibold"
								:style="{
									color: tooltipData.price_category_color,
								}"
							>
								{{ tooltipData.effective_price_category_name }}
							</span>
						</div>
						<div
							v-if="tooltipData.has_custom_price_category"
							class="text-xs text-orange-300 mt-2 bg-orange-900 bg-opacity-30 rounded px-2 py-1 text-center"
						>
							⭐ Giá đặc biệt
						</div>
						<div
							class="text-xs text-gray-400 mt-2 pt-2 border-t border-gray-700"
						>
							{{ getSeatStatusText(tooltipData.status) }}
						</div>
					</div>
				</div>
			</div>
		</Teleport>
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
const showLayoutModal = ref(false);
let timer = null;

// Tooltip state
const tooltipVisible = ref(false);
const tooltipData = ref({});
const tooltipStyle = ref({});

// Computed properties
const venueInfo = computed(() => seatMap.value?.venue || {});
const showInfo = computed(() => seatMap.value?.show || {});
const performanceData = computed(() => seatMap.value?.performance || {});
const priceCategories = computed(() => seatMap.value?.price_categories || {});

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

	return Object.values(sections).map((section) => ({
		...section,
		rows: Object.values(section.rows)
			.map((row) => ({
				...row,
				seats: sortSeatsForDisplay(row.seats, row.numbering_style),
			}))
			.sort((a, b) => {
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
	if (numberingStyle === "center_out") {
		const oddSeats = seats
			.filter((s) => {
				try {
					return parseInt(s.number) % 2 === 1;
				} catch {
					return false;
				}
			})
			.sort((a, b) => parseInt(b.number) - parseInt(a.number));

		const evenSeats = seats
			.filter((s) => {
				try {
					return parseInt(s.number) % 2 === 0;
				} catch {
					return false;
				}
			})
			.sort((a, b) => parseInt(a.number) - parseInt(b.number));

		return { oddSeats, evenSeats, style: "center_out" };
	} else {
		return {
			seats: seats.sort((a, b) => {
				try {
					return parseInt(a.number) - parseInt(b.number);
				} catch {
					return 0;
				}
			}),
			style: "linear",
		};
	}
};

const totalAmount = computed(() => {
	return selectedSeats.value.reduce(
		(sum, seat) => sum + parseFloat(seat.price),
		0
	);
});

// Seat styling
const getSeatBackgroundColor = (seat) => {
	if (isSelected(seat)) {
		return "#EAB308";
	}

	switch (seat.status) {
		case "available":
			return seat.price_category_color || "#10B981";
		case "reserved":
			return "#9CA3AF";
		case "sold":
			return "#EF4444";
		default:
			return "#D1D5DB";
	}
};

const getSeatBorderColor = (seat) => {
	if (isSelected(seat)) {
		return "#CA8A04";
	}
	return seat.price_category_color || "#10B981";
};

const getSeatClass = (seat) => {
	const classes = [];

	if (seat.status === "available") {
		classes.push(
			"hover:scale-110 cursor-pointer shadow-md hover:shadow-lg"
		);
	} else if (!isSelected(seat)) {
		classes.push("cursor-not-allowed opacity-60");
	}

	if (isSelected(seat)) {
		classes.push("ring-4 ring-yellow-400 scale-110 shadow-xl");
	}

	return classes.join(" ");
};

const isSelected = (seat) => {
	return selectedSeats.value.some((s) => s.id === seat.id);
};

// Tooltip functions
const showSeatTooltip = (seat, event) => {
	tooltipVisible.value = true;
	tooltipData.value = seat;

	const rect = event.target.getBoundingClientRect();
	const tooltipWidth = 220;

	tooltipStyle.value = {
		left: `${rect.left + rect.width / 2}px`,
		top: `${rect.top - 10}px`,
		transform: "translate(-50%, -100%)",
	};
};

const hideSeatTooltip = () => {
	tooltipVisible.value = false;
};

const getSeatStatusText = (status) => {
	const statusMap = {
		available: "✓ Còn trống",
		reserved: "⏳ Đang giữ",
		sold: "✗ Đã bán",
		blocked: "🚫 Không khả dụng",
	};
	return statusMap[status] || status;
};

// Seat selection
const toggleSeat = async (seat) => {
	if (seat.status !== "available" && !isSelected(seat)) return;

	const index = selectedSeats.value.findIndex((s) => s.id === seat.id);

	if (index > -1) {
		selectedSeats.value.splice(index, 1);

		try {
			await bookingAPI.releaseSeats([seat.id], bookingStore.sessionId);
		} catch (error) {
			console.error("Failed to release seat:", error);
		}
	} else {
		if (selectedSeats.value.length >= 8) {
			alert("Bạn chỉ có thể chọn tối đa 8 ghế");
			return;
		}

		try {
			const response = await bookingAPI.reserveSeats(
				performanceData.value.id,
				[...selectedSeats.value.map((s) => s.id), seat.id],
				bookingStore.sessionId
			);

			selectedSeats.value = response.data.seats;
			reservationExpiry.value = new Date(response.data.expires_at);

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
		console.log("Seat map data:", response.data);
	} catch (error) {
		console.error("Failed to load seat map:", error);
	}
};

// Formatting
const formatPrice = (price) => {
	return new Intl.NumberFormat("vi-VN", {
		style: "currency",
		currency: "VND",
	}).format(price);
};

const formatTime = (seconds) => {
	const mins = Math.floor(seconds / 60);
	const secs = seconds % 60;
	return `${mins}:${secs.toString().padStart(2, "0")}`;
};

// Lifecycle
onMounted(async () => {
	try {
		const savedPerformance = sessionStorage.getItem("selectedPerformance");
		if (savedPerformance) {
			performanceInfo.value = JSON.parse(savedPerformance);
		} else {
			router.push(`/booking/${route.params.showId}`);
			return;
		}

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
