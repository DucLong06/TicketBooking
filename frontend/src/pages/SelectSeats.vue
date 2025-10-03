<template>
	<DefaultLayout>
		<div
			v-if="loading"
			class="flex items-center justify-center min-h-screen"
		>
			<div class="text-center">
				<div
					class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"
				></div>
				<p class="mt-4 text-gray-600">Đang tải...</p>
			</div>
		</div>

		<div v-else class="container mx-auto px-4 py-8">
			<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
				<!-- Left Column: Seat Map (2/3 width) -->
				<div class="lg:col-span-2">
					<div
						class="bg-gradient-to-b from-gray-50 to-gray-100 rounded-2xl shadow-2xl p-6 border border-gray-200 relative overflow-hidden"
					>
						<!-- Decorative background pattern -->
						<div class="absolute inset-0 opacity-5">
							<div
								class="absolute inset-0"
								style="
									background-image: radial-gradient(
										circle,
										#000 1px,
										transparent 1px
									);
									background-size: 20px 20px;
								"
							></div>
						</div>

						<!-- Enhanced Header -->
						<div class="text-center mb-6 relative z-10">
							<h2
								class="text-3xl font-bold text-gray-800 mb-4 flex items-center justify-center gap-3"
							>
								<span class="text-4xl">🎭</span>
								<span>{{ showInfo.name }}</span>
							</h2>
							<div
								class="flex flex-wrap justify-center gap-3 text-sm"
							>
								<div
									class="flex items-center gap-2 bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full shadow-sm border border-gray-200"
								>
									<svg
										class="w-4 h-4 text-primary-600"
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
									<span class="font-semibold">{{
										performanceData.date
									}}</span>
								</div>
								<div
									class="flex items-center gap-2 bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full shadow-sm border border-gray-200"
								>
									<svg
										class="w-4 h-4 text-primary-600"
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
									<span class="font-semibold">{{
										performanceData.time
									}}</span>
								</div>
								<div
									class="flex items-center gap-2 bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full shadow-sm border border-gray-200"
								>
									<svg
										class="w-4 h-4 text-primary-600"
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
									<span class="font-medium">{{
										venueInfo.name
									}}</span>
								</div>
								<div
									v-if="showInfo.duration_minutes"
									class="flex items-center gap-2 bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full shadow-sm border border-gray-200"
								>
									<svg
										class="w-4 h-4 text-primary-600"
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
									<span class="font-medium"
										>{{
											showInfo.duration_minutes
										}}
										phút</span
									>
								</div>
							</div>
							<div
								v-if="venueInfo.checkin_minutes_before"
								class="mt-3 inline-block"
							>
								<div
									class="bg-amber-100/80 backdrop-blur-sm border-2 border-amber-300 rounded-full px-4 py-2 shadow-sm"
								>
									<span
										class="text-xs text-amber-800 font-semibold"
									>
										⏰ Vui lòng có mặt trước
										{{ venueInfo.checkin_minutes_before }}
										phút
									</span>
								</div>
							</div>
						</div>

						<!-- Compact Floating Zoom Controls -->
						<div class="absolute top-4 right-4 z-20">
							<div
								class="bg-white/95 backdrop-blur-md rounded-xl shadow-2xl border border-gray-200 p-2"
							>
								<div class="flex flex-col gap-1">
									<!-- Zoom In -->
									<button
										@click="zoomIn"
										:disabled="zoomLevel >= 1.5"
										class="w-10 h-10 rounded-lg bg-gradient-to-br from-primary-50 to-primary-100 hover:from-primary-100 hover:to-primary-200 disabled:opacity-40 disabled:cursor-not-allowed transition-all flex items-center justify-center group"
										title="Phóng to"
									>
										<svg
											class="w-5 h-5 text-primary-600 group-disabled:text-gray-400"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2.5"
												d="M12 4v16m8-8H4"
											/>
										</svg>
									</button>

									<!-- Zoom Level Display -->
									<div
										class="text-center py-1 px-2 text-xs font-bold text-primary-600 bg-primary-50 rounded"
									>
										{{ Math.round(zoomLevel * 100) }}%
									</div>

									<!-- Zoom Out -->
									<button
										@click="zoomOut"
										:disabled="zoomLevel <= 0.25"
										class="w-10 h-10 rounded-lg bg-gradient-to-br from-primary-50 to-primary-100 hover:from-primary-100 hover:to-primary-200 disabled:opacity-40 disabled:cursor-not-allowed transition-all flex items-center justify-center group"
										title="Thu nhỏ"
									>
										<svg
											class="w-5 h-5 text-primary-600 group-disabled:text-gray-400"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2.5"
												d="M20 12H4"
											/>
										</svg>
									</button>

									<!-- Reset -->
									<button
										@click="resetZoom"
										class="w-10 h-10 rounded-lg bg-gradient-to-br from-amber-50 to-amber-100 hover:from-amber-100 hover:to-amber-200 transition-all flex items-center justify-center group mt-1 border-t border-gray-200 pt-1"
										title="Đặt lại"
									>
										<svg
											class="w-4 h-4 text-amber-600"
											fill="none"
											stroke="currentColor"
											viewBox="0 0 24 24"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2.5"
												d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
											/>
										</svg>
									</button>
								</div>
							</div>
						</div>

						<!-- Seat Map Container with Zoom -->
						<div
							class="relative bg-white rounded-2xl shadow-inner border-2 border-gray-200 overflow-hidden"
							style="min-height: 500px; max-height: 650px"
						>
							<!-- Theater ambiance overlay -->
							<div
								class="absolute inset-0 bg-gradient-to-b from-purple-900/5 via-transparent to-gray-900/5 pointer-events-none"
							></div>

							<div
								class="overflow-auto h-full p-6"
								id="seat-map-container"
							>
								<div
									class="transition-transform duration-300 ease-out"
									:style="{
										transform: `scale(${zoomLevel})`,
										transformOrigin: 'top center',
										minWidth: 'fit-content',
										margin: '0 auto',
									}"
								>
									<!-- Stage - Now inside zoom area -->
									<div class="mb-12 flex justify-center">
										<div
											class="relative"
											:style="{ width: stageWidth }"
										>
											<!-- Stage lighting effect -->
											<div
												class="absolute -top-8 left-1/2 transform -translate-x-1/2 w-3/4 h-16 bg-gradient-radial from-yellow-200/30 via-transparent to-transparent blur-xl"
											></div>

											<!-- Main stage -->
											<div
												class="relative bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 text-white py-6 px-8 rounded-t-2xl text-center shadow-2xl border-t-4 border-yellow-500/50"
											>
												<!-- Curtain effect -->
												<div
													class="absolute inset-0 bg-gradient-to-b from-red-900/20 to-transparent rounded-t-2xl"
												></div>

												<!-- Stage content -->
												<div class="relative z-10">
													<div
														class="text-2xl font-bold tracking-wider mb-1 text-yellow-100"
													>
														SÂN KHẤU
													</div>
													<div
														class="text-sm opacity-75 tracking-widest text-yellow-200/70"
													>
														STAGE
													</div>
												</div>

												<!-- Stage floor line -->
												<div
													class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-yellow-500/50 to-transparent"
												></div>
											</div>

											<!-- Stage apron/edge -->
											<div
												class="h-2 bg-gradient-to-b from-gray-700 to-gray-600 rounded-b-sm shadow-lg"
											></div>
										</div>
									</div>

									<!-- Main area with LG -->
									<div
										class="flex items-start justify-between gap-20"
									>
										<!-- LG Left -->
										<div
											v-if="logeLeftSection"
											class="flex-shrink-0"
											style="width: 50px"
										>
											<div
												:style="{
													marginTop: lgMarginTop,
												}"
											>
												<div
													class="text-center mb-2 text-xs font-bold text-gray-500"
												>
													LG
												</div>
												<div
													class="flex flex-col gap-2"
												>
													<button
														v-for="seat in logeLeftSection.seats"
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
															'w-12 h-12 text-xs font-bold rounded-lg border-2 transition-all duration-200',
															getSeatClass(seat),
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
										</div>
										<!-- Main Sections -->
										<div
											class="flex-1"
											style="
												max-width: 1000px;
												margin: 0 260px;
											"
										>
											<div
												v-for="section in mainSections"
												:key="section.id"
												class="mb-10"
											>
												<!-- Section header -->
												<div class="text-center mb-6">
													<div
														class="inline-block bg-gradient-to-r from-primary-500 to-purple-500 text-white px-6 py-2 rounded-full shadow-lg"
													>
														<h3
															class="font-bold text-lg tracking-wide"
														>
															{{ section.name }}
														</h3>
													</div>
												</div>

												<!-- Rows -->
												<div
													class="flex flex-col items-center"
												>
													<div
														v-for="row in section.rows"
														:key="row.label"
														:ref="
															(el) => {
																if (el)
																	rowRefs[
																		`${section.id}-${row.label}`
																	] = el;
															}
														"
														class="flex items-center justify-center"
														:style="{
															marginBottom:
																row.spacing_after
																	? `${row.spacing_after}px`
																	: '16px',
														}"
													>
														<!-- Row Label Left -->
														<span
															class="w-12 text-right mr-6 font-bold text-gray-600 text-base"
														>
															{{ row.label }}
														</span>

														<!-- Seats Container -->
														<div
															class="flex justify-center"
														>
															<!-- Center-out layout -->
															<div
																v-if="
																	row.seats
																		.style ===
																	'center_out'
																"
																class="flex gap-2 items-center"
															>
																<!-- Left side (odd) -->
																<button
																	v-for="seat in row
																		.seats
																		.oddSeats"
																	:key="
																		seat.id
																	"
																	@click="
																		toggleSeat(
																			seat
																		)
																	"
																	:disabled="
																		seat.status !==
																			'available' &&
																		!isSelected(
																			seat
																		)
																	"
																	:class="[
																		'w-10 h-10 text-sm font-bold rounded-lg border-2 transition-all duration-200',
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
																				: '3px',
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
																<div
																	class="w-12 flex items-center justify-center"
																>
																	<div
																		class="w-px h-8 bg-gradient-to-b from-transparent via-gray-300 to-transparent"
																	></div>
																</div>

																<!-- Right side (even) -->
																<button
																	v-for="seat in row
																		.seats
																		.evenSeats"
																	:key="
																		seat.id
																	"
																	@click="
																		toggleSeat(
																			seat
																		)
																	"
																	:disabled="
																		seat.status !==
																			'available' &&
																		!isSelected(
																			seat
																		)
																	"
																	:class="[
																		'w-10 h-10 text-sm font-bold rounded-lg border-2 transition-all duration-200',
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
																				: '3px',
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
																class="flex gap-2 items-center"
															>
																<button
																	v-for="seat in row
																		.seats
																		.seats"
																	:key="
																		seat.id
																	"
																	@click="
																		toggleSeat(
																			seat
																		)
																	"
																	:disabled="
																		seat.status !==
																			'available' &&
																		!isSelected(
																			seat
																		)
																	"
																	:class="[
																		'w-10 h-10 text-sm font-bold rounded-lg border-2 transition-all duration-200',
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
																				: '3px',
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
															class="w-12 text-left ml-6 font-bold text-gray-600 text-base"
														>
															{{ row.label }}
														</span>
													</div>
												</div>
											</div>
										</div>

										<!-- LG Right -->
										<div
											v-if="logeRightSection"
											class="flex-shrink-0"
											style="width: 50px"
										>
											<div
												:style="{
													marginTop: lgMarginTop,
												}"
											>
												<div
													class="text-center mb-2 text-xs font-bold text-gray-500"
												>
													LG
												</div>
												<div
													class="flex flex-col gap-2"
												>
													<button
														v-for="seat in logeRightSection.seats"
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
															'w-12 h-12 text-xs font-bold rounded-lg border-2 transition-all duration-200',
															getSeatClass(seat),
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
										</div>
									</div>
								</div>
							</div>
						</div>

						<!-- Status Legend -->
						<div
							class="mt-6 bg-white/90 backdrop-blur-sm rounded-xl shadow-lg p-5 border border-gray-200 relative z-10"
						>
							<h4
								class="font-bold mb-4 text-gray-700 text-center text-lg"
							>
								📌 Trạng thái ghế
							</h4>
							<div class="grid grid-cols-2 md:grid-cols-4 gap-3">
								<div
									class="flex items-center space-x-3 bg-green-50 p-3 rounded-lg border border-green-200"
								>
									<div
										class="w-8 h-8 bg-green-500 rounded-lg border-2 border-green-600 shadow-sm flex-shrink-0"
									></div>
									<span
										class="text-sm font-medium text-gray-700"
										>Còn trống</span
									>
								</div>
								<div
									class="flex items-center space-x-3 bg-yellow-50 p-3 rounded-lg border border-yellow-200"
								>
									<div
										class="w-8 h-8 bg-yellow-500 rounded-lg border-2 border-yellow-600 shadow-sm flex-shrink-0"
									></div>
									<span
										class="text-sm font-medium text-gray-700"
										>Đang chọn</span
									>
								</div>
								<div
									class="flex items-center space-x-3 bg-red-50 p-3 rounded-lg border border-red-200"
								>
									<div
										class="w-8 h-8 bg-red-500 rounded-lg border-2 border-red-600 shadow-sm flex-shrink-0"
									></div>
									<span
										class="text-sm font-medium text-gray-700"
										>Đã bán</span
									>
								</div>
								<div
									class="flex items-center space-x-3 bg-gray-50 p-3 rounded-lg border border-gray-200"
								>
									<div
										class="w-8 h-8 bg-gray-400 rounded-lg border-2 border-gray-500 shadow-sm flex-shrink-0"
									></div>
									<span
										class="text-sm font-medium text-gray-700"
										>Đang giữ</span
									>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Right Column: Price Categories & Booking Summary -->
				<div class="lg:col-span-1">
					<!-- Price Categories -->
					<div
						class="mb-6 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 rounded-2xl shadow-xl p-5 border-2 border-blue-100"
					>
						<h3
							class="font-bold mb-4 text-gray-800 text-center text-lg flex items-center justify-center gap-2"
						>
							<span class="text-xl">📋</span>
							<span>Phân loại vé</span>
						</h3>
						<div class="space-y-3">
							<div
								v-for="(category, code) in priceCategories"
								:key="code"
								class="flex items-center justify-between bg-white/80 backdrop-blur-sm rounded-xl p-3 shadow-md border border-gray-100 hover:shadow-lg transition-shadow"
							>
								<div class="flex items-center gap-3">
									<div
										class="w-6 h-6 rounded-lg border-2 border-white shadow-md flex-shrink-0"
										:style="{
											backgroundColor: category.color,
										}"
									></div>
									<div
										class="text-sm font-semibold text-gray-800"
									>
										{{ category.name }}
									</div>
								</div>
								<div class="text-sm text-primary-600 font-bold">
									{{ formatPrice(category.price) }}
								</div>
							</div>
						</div>
					</div>

					<!-- Booking Summary -->
					<div
						class="bg-white rounded-2xl shadow-2xl p-6 sticky top-4 border-2 border-gray-100"
					>
						<!-- Layout Image Button -->
						<div v-if="venueInfo.layout_image_url" class="mb-6">
							<button
								@click="showLayoutModal = true"
								class="w-full py-3 px-4 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 text-white rounded-xl font-semibold hover:from-blue-600 hover:via-purple-600 hover:to-pink-600 transition-all flex items-center justify-center gap-2 shadow-lg hover:shadow-xl transform hover:scale-105"
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
						<div class="mb-4 pb-4 border-b-2 border-gray-100">
							<h4
								class="font-bold mb-3 text-gray-800 flex items-center gap-2"
							>
								<span class="text-lg">🎫</span>
								<span>Ghế đã chọn</span>
							</h4>
							<div
								v-if="selectedSeats.length === 0"
								class="text-center py-8 text-gray-400 bg-gray-50 rounded-xl"
							>
								<svg
									class="w-12 h-12 mx-auto mb-2 opacity-50"
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
								<p class="text-sm">Chưa chọn ghế nào</p>
							</div>
							<div
								v-else
								class="space-y-2 max-h-60 overflow-y-auto pr-2 custom-scrollbar"
							>
								<div
									v-for="seat in selectedSeats"
									:key="seat.id"
									class="flex justify-between items-center text-sm bg-gradient-to-r from-primary-50 to-purple-50 p-3 rounded-xl border-2 border-primary-200 shadow-sm hover:shadow-md transition-shadow"
								>
									<span class="font-bold text-gray-800">{{
										seat.full_label
									}}</span>
									<span class="text-primary-600 font-bold">{{
										formatPrice(seat.price)
									}}</span>
								</div>
							</div>
						</div>

						<!-- Total -->
						<div class="mb-4 pb-4 border-b-2 border-gray-100">
							<div
								class="flex justify-between items-center bg-gradient-to-r from-green-50 to-emerald-50 p-4 rounded-xl shadow-md border-2 border-green-200"
							>
								<span class="font-bold text-gray-700 text-lg"
									>Tổng tiền:</span
								>
								<span
									class="text-2xl font-bold text-green-600"
									>{{ formatPrice(totalAmount) }}</span
								>
							</div>
						</div>

						<!-- Timer -->
						<div
							v-if="timeLeft > 0"
							class="mb-4 p-4 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-xl border-2 border-yellow-300 shadow-md"
						>
							<div class="text-sm text-yellow-800 text-center">
								<div
									class="font-semibold mb-2 flex items-center justify-center gap-2"
								>
									<span class="text-lg">⏱️</span>
									<span>Thời gian giữ ghế</span>
								</div>
								<div
									class="text-3xl font-bold text-orange-600 tabular-nums"
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
								'w-full py-4 px-4 rounded-xl font-bold text-lg transition-all shadow-xl',
								selectedSeats.length > 0
									? 'bg-gradient-to-r from-green-500 via-emerald-500 to-teal-500 text-white hover:from-green-600 hover:via-emerald-600 hover:to-teal-600 hover:shadow-2xl transform hover:scale-105 active:scale-95'
									: 'bg-gray-200 text-gray-400 cursor-not-allowed',
							]"
						>
							{{
								selectedSeats.length > 0
									? `Tiếp tục (${selectedSeats.length} ghế)`
									: "Chọn ghế để tiếp tục"
							}}
						</button>
					</div>
				</div>
			</div>
		</div>

		<!-- Layout Image Modal -->
		<Teleport to="body">
			<div
				v-if="showLayoutModal"
				class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-fade-in"
				@click="showLayoutModal = false"
			>
				<div
					class="relative max-w-5xl w-full bg-white rounded-2xl shadow-2xl animate-scale-in"
					@click.stop
				>
					<button
						@click="showLayoutModal = false"
						class="absolute -top-4 -right-4 bg-white rounded-full p-3 shadow-2xl hover:bg-gray-100 transition-all hover:scale-110 z-10"
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
						<h3
							class="text-2xl font-bold mb-4 text-gray-800 flex items-center gap-2"
						>
							<span class="text-3xl">🏛️</span>
							<span>Sơ đồ {{ venueInfo.name }}</span>
						</h3>
						<img
							:src="venueInfo.layout_image_url"
							alt="Venue Layout"
							class="w-full rounded-xl shadow-2xl"
						/>
					</div>
				</div>
			</div>
		</Teleport>

		<!-- Seat Tooltip -->
		<Teleport to="body">
			<div
				v-if="tooltipVisible"
				:style="tooltipStyle"
				class="fixed z-50 pointer-events-none animate-fade-in"
			>
				<div
					class="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white rounded-2xl shadow-2xl border-2 border-gray-600 overflow-hidden"
					style="min-width: 240px; max-width: 280px"
				>
					<!-- Seat Image -->
					<div
						v-if="tooltipData.seat_image_url"
						class="w-full h-36 overflow-hidden"
					>
						<img
							:src="tooltipData.seat_image_url"
							alt="Seat View"
							class="w-full h-full object-cover"
						/>
					</div>

					<!-- Seat Info -->
					<div class="p-4">
						<div
							class="font-bold text-xl mb-3 text-yellow-300 flex items-center gap-2"
						>
							<span>🎫</span>
							<span>{{ tooltipData.full_label }}</span>
						</div>
						<div class="space-y-2 text-sm">
							<div
								class="flex items-center justify-between bg-white/10 rounded-lg p-2"
							>
								<span class="text-gray-300">Giá:</span>
								<span
									class="font-bold text-green-400 text-lg"
									>{{ formatPrice(tooltipData.price) }}</span
								>
							</div>
							<div
								class="flex items-center justify-between bg-white/10 rounded-lg p-2"
							>
								<span class="text-gray-300">Loại:</span>
								<span
									class="font-semibold"
									:style="{
										color: tooltipData.price_category_color,
									}"
								>
									{{
										tooltipData.effective_price_category_name
									}}
								</span>
							</div>
							<div
								class="text-xs text-gray-400 pt-2 border-t border-gray-700 text-center"
							>
								{{ getSeatStatusText(tooltipData.status) }}
							</div>
						</div>
					</div>
				</div>
			</div>
		</Teleport>
	</DefaultLayout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from "vue";
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

// Zoom state
const zoomLevel = ref(1);

// Tooltip state
const tooltipVisible = ref(false);
const tooltipData = ref({});
const tooltipStyle = ref({});

// Row refs for calculating stage width
const rowRefs = ref({});

// Computed properties
const venueInfo = computed(() => seatMap.value?.venue || {});
const showInfo = computed(() => seatMap.value?.show || {});
const performanceData = computed(() => seatMap.value?.performance || {});
const priceCategories = computed(() => seatMap.value?.price_categories || {});

// Calculate stage width based on longest row
const stageWidth = computed(() => {
	if (Object.keys(rowRefs.value).length === 0) return "90%";

	let maxWidth = 0;
	Object.values(rowRefs.value).forEach((rowEl) => {
		if (rowEl && rowEl.offsetWidth) {
			const seatsContainer = rowEl.querySelector(".flex.justify-center");
			if (seatsContainer) {
				const width = seatsContainer.offsetWidth;
				if (width > maxWidth) maxWidth = width;
			}
		}
	});

	return maxWidth > 0 ? `${maxWidth + 40}px` : "90%";
});

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
				position_y: seat.row_position_y,
				spacing_after: seat.row_spacing_after,
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
			.sort((a, b) => a.position_y - b.position_y),
	}));
});

const mainSections = computed(() => {
	if (!seatsBySections.value) return [];
	return seatsBySections.value.filter(
		(s) => s.id !== "loge_left" && s.id !== "loge_right"
	);
});

const logeLeftSection = computed(() => {
	if (!seatsBySections.value) return null;
	const section = seatsBySections.value.find((s) => s.id === "loge_left");
	if (!section || !section.rows || section.rows.length === 0) return null;

	const row = section.rows[0];
	let seats =
		row.seats.style === "linear"
			? row.seats.seats || []
			: [
					...(row.seats.oddSeats || []),
					...(row.seats.evenSeats || []),
			  ].sort((a, b) => parseInt(a.number) - parseInt(b.number));

	console.log("=== LOGE LEFT DEBUG ===");
	console.log("Total seats:", seats.length);
	seats.forEach((seat) => {
		console.log(`Seat ${seat.number}: position_y=${seat.position_y}`);
	});
	return { id: section.id, name: section.name, seats };
});

const logeRightSection = computed(() => {
	if (!seatsBySections.value) return null;
	const section = seatsBySections.value.find((s) => s.id === "loge_right");
	if (!section || !section.rows || section.rows.length === 0) return null;

	const row = section.rows[0];
	let seats =
		row.seats.style === "linear"
			? row.seats.seats || []
			: [
					...(row.seats.oddSeats || []),
					...(row.seats.evenSeats || []),
			  ].sort((a, b) => parseInt(a.number) - parseInt(b.number));

	return { id: section.id, name: section.name, seats };
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

// Zoom functions
const zoomIn = () => {
	if (zoomLevel.value < 1.5) {
		zoomLevel.value = Math.min(1.5, zoomLevel.value + 0.1);
	}
};

const zoomOut = () => {
	if (zoomLevel.value > 0.25) {
		zoomLevel.value = Math.max(0.25, zoomLevel.value - 0.1);
	}
};

const resetZoom = () => {
	zoomLevel.value = 1;
};

// Seat styling
const getSeatBackgroundColor = (seat) => {
	if (isSelected(seat)) return "#EAB308";
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
	if (isSelected(seat)) return "#CA8A04";
	return seat.price_category_color || "#10B981";
};

const getSeatClass = (seat) => {
	const classes = [];
	if (seat.status === "available") {
		classes.push(
			"hover:scale-110 cursor-pointer shadow-md hover:shadow-xl"
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
		await nextTick();
	} catch (error) {
		console.error("Failed to load seat map:", error);
	}
};
const lgMarginTop = computed(() => {
	const rowHeight = window.innerWidth < 768 ? 35 : 45;
	const startFromRow = 12;
	return `${startFromRow * rowHeight}px`;
});
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
	if (timer) clearInterval(timer);
});
</script>

<style scoped>
/* Custom slider styling */
.slider-thumb::-webkit-slider-thumb {
	-webkit-appearance: none;
	appearance: none;
	width: 20px;
	height: 20px;
	border-radius: 50%;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	cursor: pointer;
	box-shadow: 0 2px 8px rgba(102, 126, 234, 0.6);
	transition: all 0.2s ease;
}

.slider-thumb::-webkit-slider-thumb:hover {
	transform: scale(1.2);
	box-shadow: 0 4px 12px rgba(102, 126, 234, 0.8);
}

.slider-thumb::-moz-range-thumb {
	width: 20px;
	height: 20px;
	border-radius: 50%;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	cursor: pointer;
	box-shadow: 0 2px 8px rgba(102, 126, 234, 0.6);
	transition: all 0.2s ease;
	border: none;
}

.slider-thumb::-moz-range-thumb:hover {
	transform: scale(1.2);
	box-shadow: 0 4px 12px rgba(102, 126, 234, 0.8);
}

/* Custom scrollbar */
.custom-scrollbar::-webkit-scrollbar {
	width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
	background: #f1f1f1;
	border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
	background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
	border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
	background: linear-gradient(180deg, #764ba2 0%, #667eea 100%);
}

/* Animations */
@keyframes fade-in {
	from {
		opacity: 0;
	}
	to {
		opacity: 1;
	}
}

@keyframes scale-in {
	from {
		transform: scale(0.95);
		opacity: 0;
	}
	to {
		transform: scale(1);
		opacity: 1;
	}
}

.animate-fade-in {
	animation: fade-in 0.2s ease-out;
}

.animate-scale-in {
	animation: scale-in 0.3s ease-out;
}
</style>
