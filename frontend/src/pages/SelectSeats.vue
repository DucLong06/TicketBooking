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
					<div class="">
						<!-- Price Categories - Mobile horizontal scroll -->
						<div class="lg:hidden mb-4">
							<div class="grid grid-cols-2 gap-2">
								<div
									v-for="(category, code) in priceCategories"
									:key="code"
									class="flex items-center gap-2 bg-white/90 backdrop-blur-sm rounded-lg px-2.5 py-2 shadow-sm border border-gray-200"
								>
									<div
										class="w-3.5 h-3.5 rounded border border-white shadow-sm flex-shrink-0"
										:style="{
											backgroundColor: category.color,
										}"
									></div>
									<div class="text-xs flex-1 min-w-0">
										<div
											class="font-semibold text-gray-800 truncate"
										>
											{{ category.name }}
										</div>
										<div class="text-gray-600 text-xs">
											{{ formatPrice(category.price) }}
										</div>
									</div>
								</div>
							</div>
						</div>

						<!-- Seat Map Container with Zoom -->

						<div
							class="relative overflow-hidden"
							style="min-height: 500px; max-height: 650px"
						>
							<!-- Zoom Controls - Top Left Corner -->
							<div
								class="absolute top-4 left-4 z-20 flex flex-col gap-2"
							>
								<button
									@click="handleZoomIn"
									class="bg-white hover:bg-gray-100 text-gray-700 p-3 rounded-lg shadow-lg border-2 border-gray-200 transition-all hover:scale-110 active:scale-95"
									title="Phóng to"
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
											d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v6m3-3H7"
										/>
									</svg>
								</button>

								<button
									@click="handleZoomOut"
									class="bg-white hover:bg-gray-100 text-gray-700 p-3 rounded-lg shadow-lg border-2 border-gray-200 transition-all hover:scale-110 active:scale-95"
									title="Thu nhỏ"
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
											d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM13 10H7"
										/>
									</svg>
								</button>

								<button
									@click="handleResetView"
									class="bg-white hover:bg-gray-100 text-gray-700 p-3 rounded-lg shadow-lg border-2 border-gray-200 transition-all hover:scale-110 active:scale-95"
									title="Đặt lại vị trí"
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
											d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
										/>
									</svg>
								</button>
							</div>

							<div class=""></div>

							<div
								class="h-full p-6 flex items-center justify-center"
								id="seat-map-container"
								@wheel="handleWheel"
								@mousedown="handleMouseDown"
								@mousemove="handleMouseMove"
								@mouseup="handleMouseUp"
								@mouseleave="handleMouseLeave"
								@touchstart="handleTouchStart"
								@touchmove="handleTouchMove"
								@touchend="handleTouchEnd"
								:style="{
									cursor: isDragging ? 'grabbing' : 'grab',
									userSelect: 'none',
									touchAction: 'none',
								}"
							>
								<div
									:class="[
										'ease-out',
										{
											'transition-transform duration-200':
												!isDragging,
											'transition-transform duration-500':
												zoomLevel <= 0.25,
										},
									]"
									:style="{
										transform: `translate(${panX}px, ${panY}px) scale(${zoomLevel})`,
										transformOrigin: 'center center',
										minWidth: 'fit-content',
										margin: '0 auto',
									}"
								>
									<!-- Stage -->
									<div class="mb-12 flex justify-center">
										<div
											class="relative"
											:style="{ width: stageWidth }"
										>
											<div
												class="absolute -top-8 left-1/2 transform -translate-x-1/2 w-3/4 h-16 bg-gradient-radial from-yellow-200/30 via-transparent to-transparent blur-xl"
											></div>
											<div
												class="relative bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 text-white py-6 px-8 rounded-t-2xl text-center shadow-2xl border-t-4 border-yellow-500/50"
											>
												<div
													class="absolute inset-0 bg-gradient-to-b from-red-900/20 to-transparent rounded-t-2xl"
												></div>
												<div class="relative z-10">
													<div
														class="text-4xl font-bold tracking-wider mb-1 text-yellow-100"
													>
														SÂN KHẤU
													</div>
													<div
														class="text-xl opacity-75 tracking-widest text-yellow-200/70"
													>
														STAGE
													</div>
												</div>
												<div
													class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-yellow-500/50 to-transparent"
												></div>
											</div>
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
														<span
															class="w-12 text-right mr-6 font-bold text-gray-600 text-base"
														>
															{{ row.label }}
														</span>

														<div
															class="flex justify-center"
														>
															<div
																v-if="
																	row.seats
																		.style ===
																	'center_out'
																"
																class="flex gap-2 items-center"
															>
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

																<div
																	class="w-12 flex items-center justify-center"
																>
																	<div
																		class="w-px h-8 bg-gradient-to-b from-transparent via-gray-300 to-transparent"
																	></div>
																</div>

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
						<!-- <div
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
						</div> -->
					</div>
				</div>

				<!-- Right Column: Price Categories & Booking Summary - DESKTOP ONLY -->

				<div class="hidden lg:block lg:col-span-1">
					<!-- Decorative background pattern -->
					<!-- <div class="absolute inset-0 opacity-5">
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
					</div> -->

					<!-- Enhanced Header -->

					<div
						class="mb-6 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 rounded-2xl shadow-xl p-5 border-2 border-blue-100"
					>
						<div class="text-center relative z-10">
							<h2
								class="text-xl lg:text-2xl font-bold text-gray-800 mb-3 lg:mb-4 flex items-center justify-center gap-2 lg:gap-3"
							>
								<span class="text-2xl lg:text-3xl">🎭</span>
								<span>{{ showInfo.name }}</span>
							</h2>
							<div
								class="flex flex-wrap justify-center gap-2 lg:gap-3 text-xs"
							>
								<div
									class="flex items-center gap-1.5 lg:gap-2 bg-white/80 backdrop-blur-sm px-3 lg:px-4 py-1.5 lg:py-2 rounded-full shadow-sm border border-gray-200"
								>
									<svg
										class="w-3.5 h-3.5 lg:w-4 lg:h-4 text-primary-600"
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
									class="flex items-center gap-1.5 lg:gap-2 bg-white/80 backdrop-blur-sm px-3 lg:px-4 py-1.5 lg:py-2 rounded-full shadow-sm border border-gray-200"
								>
									<svg
										class="w-3.5 h-3.5 lg:w-4 lg:h-4 text-primary-600"
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
									class="hidden lg:flex items-center gap-2 bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full shadow-sm border border-gray-200"
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
									class="hidden lg:flex items-center gap-2 bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full shadow-sm border border-gray-200"
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
								class="mt-2 lg:mt-3 inline-block"
							>
								<!-- <div
									class="bg-amber-100/80 backdrop-blur-sm border-2 border-amber-300 rounded-full px-3 lg:px-4 py-1.5 lg:py-2 shadow-sm"
								>
									<span
										class="text-xs text-amber-800 font-semibold"
									>
										Vé không kèm trẻ em, chương trình không
										dành cho trẻ em dưới 6 tuổi
									</span>
								</div> -->
							</div>
						</div>
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

					<div
						class="bg-white rounded-2xl shadow-2xl p-6 sticky top-4 border-2 border-gray-100"
					>
						<div class="mb-4 pb-4 border-b-2 border-gray-100">
							<h4
								class="font-bold mb-3 text-gray-800 flex items-center gap-2"
							>
								<span class="text-lg">🎫</span>
								<span>Ghế đã chọn</span>
							</h4>

							<div
								class="space-y-2 max-h-60 overflow-y-auto pr-2 custom-scrollbar"
							>
								<div
									v-for="seat in selectedSeats"
									:key="seat.id"
									class="flex justify-between items-center text-sm bg-gradient-to-r from-primary-50 to-purple-50 p-3 rounded-xl border-2 border-primary-200 shadow-sm hover:shadow-md transition-shadow"
								>
									<span class="font-bold text-gray-800">{{
										seat.full_label +
										" - " +
										seat.section_name
									}}</span>
									<span class="text-primary-600 font-bold">{{
										formatPrice(seat.price)
									}}</span>
								</div>
							</div>
						</div>

						<div class="mb-4">
							<div
								v-if="selectedSeats.length !== 0"
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

		<!-- Mobile Bottom Sheet -->
		<div class="lg:hidden">
			<div
				v-if="bottomSheetState === 'expanded'"
				class="fixed inset-0 bg-black/40 z-40 transition-opacity"
				@click="bottomSheetState = 'minimized'"
			></div>

			<div
				v-if="selectedSeats.length > 0"
				class="fixed bottom-0 left-0 right-0 bg-white rounded-t-3xl shadow-2xl z-50 transition-transform duration-300"
				:style="{
					transform: getBottomSheetTransform(),
				}"
				@touchstart="handleBottomSheetTouchStart"
				@touchmove="handleBottomSheetTouchMove"
				@touchend="handleBottomSheetTouchEnd"
			>
				<div class="flex justify-center pt-3 pb-2">
					<div class="w-12 h-1 bg-gray-300 rounded-full"></div>
				</div>

				<div v-if="bottomSheetState === 'minimized'" class="px-4 pb-4">
					<div class="flex items-center justify-between gap-3">
						<div
							class="flex-1 cursor-pointer flex items-center gap-3"
							@click="bottomSheetState = 'expanded'"
						>
							<span class="text-purple-600 text-xl">🎫</span>
							<div>
								<div class="font-bold text-gray-800">
									{{ selectedSeats.length }} ghế đã chọn
								</div>
								<div class="text-sm text-gray-600">
									{{ formatPrice(totalAmount) }}
								</div>
							</div>
						</div>

						<div class="text-center flex-shrink-0">
							<div
								class="text-lg font-bold text-orange-600 tabular-nums"
							>
								{{ formatTime(timeLeft) }}
							</div>
						</div>

						<button
							@click.stop="continueToCustomerInfo"
							class="bg-gradient-to-r from-green-500 to-teal-500 text-white px-4 py-2 rounded-lg font-bold text-sm shadow-lg hover:shadow-xl transform active:scale-95 transition-all flex-shrink-0"
						>
							Tiếp tục
						</button>
					</div>
				</div>

				<div
					v-if="bottomSheetState === 'expanded'"
					class="px-4 pb-4 pt-2"
				>
					<div class="flex justify-center mb-3">
						<button
							@click="bottomSheetState = 'minimized'"
							class="p-2 hover:bg-gray-100 rounded-full"
						>
							<svg
								class="w-5 h-5 text-gray-400"
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

					<div class="grid grid-cols-4 gap-2 items-stretch mb-3">
						<div
							class="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-xl border-2 border-yellow-300 p-3 text-center flex flex-col justify-center"
						>
							<div
								class="text-xs text-yellow-800 font-semibold mb-1"
							>
								⏱️
							</div>
							<div
								class="text-sm font-bold text-orange-600 mb-0.5"
							>
								{{ formatTime(timeLeft) }}
							</div>
							<div class="text-xs text-yellow-700">Giữ ghế</div>
						</div>

						<div
							class="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl border-2 border-purple-300 p-3 text-center flex flex-col justify-center"
						>
							<div
								class="text-xs text-purple-800 font-semibold mb-1"
							>
								🎫
							</div>
							<div
								class="text-lg font-bold text-purple-600 mb-0.5"
							>
								{{ selectedSeats.length }}
							</div>
							<div class="text-xs text-purple-700">Đã chọn</div>
						</div>

						<div
							class="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl border-2 border-green-300 p-3 text-center flex flex-col justify-center"
						>
							<div
								class="text-xs text-green-800 font-semibold mb-1"
							>
								💰
							</div>
							<div
								class="text-sm font-bold text-green-600 mb-0.5 leading-tight"
							>
								{{ (totalAmount / 1000).toFixed(0) }}K
							</div>
							<div class="text-xs text-green-700">Tổng tiền</div>
						</div>

						<button
							@click="continueToCustomerInfo"
							class="bg-gradient-to-r from-green-500 via-emerald-500 to-teal-500 text-white rounded-xl font-bold text-sm shadow-lg hover:shadow-xl transform active:scale-95 transition-all flex items-center justify-center px-2"
						>
							Tiếp tục →
						</button>
					</div>

					<details class="mt-3">
						<summary
							class="text-xs text-gray-600 cursor-pointer hover:text-gray-800 text-center py-2"
						>
							Xem chi tiết ghế đã chọn ▼
						</summary>
						<div class="space-y-2 mt-2 max-h-40 overflow-y-auto">
							<div
								v-for="seat in selectedSeats"
								:key="seat.id"
								class="flex justify-between items-center bg-gradient-to-r from-purple-50 to-blue-50 p-2 rounded-lg border border-purple-200 text-xs"
							>
								<div>
									<div class="font-bold text-gray-800">
										{{ seat.full_label }}
									</div>
									<div class="text-gray-600">
										{{ seat.section_name }}
									</div>
								</div>
								<div class="font-bold text-purple-600">
									{{ formatPrice(seat.price) }}
								</div>
							</div>
						</div>
					</details>
				</div>
			</div>
		</div>

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

const isMobile = ref(window.innerWidth < 1024);

// State
const loading = ref(true);
const seatMap = ref(null);
const selectedSeats = ref([]);
const performanceInfo = ref({});
const reservationExpiry = ref(null);
const timeLeft = ref(0);
const showLayoutModal = ref(false);
let timer = null;

// Zoom and Pan state
const zoomLevel = ref(0.29);
const panX = ref(0);
const panY = ref(-770);
const initialZoomLevel = ref(0.29);
const initialPanX = ref(0);
const initialPanY = ref(-770);

const isDragging = ref(false);
const dragStart = ref({ x: 0, y: 0 });
const lastTouchDistance = ref(0);
const lastTouchCenter = ref({ x: 0, y: 0 });

// Tooltip state
const tooltipVisible = ref(false);
const tooltipData = ref({});
const tooltipStyle = ref({});
let tooltipTimer = null;

// Row refs for calculating stage width
const rowRefs = ref({});

// Mobile bottom sheet state
const bottomSheetState = ref("minimized");
const touchStart = ref(null);
const touchOffset = ref(0);

// Zoom instructions state
const showZoomInstructions = ref(false);
const instructionsClosed = ref(false);

// Computed properties
const venueInfo = computed(() => seatMap.value?.venue || {});
const showInfo = computed(() => seatMap.value?.show || {});
const performanceData = computed(() => seatMap.value?.performance || {});
const priceCategories = computed(() => seatMap.value?.price_categories || {});

const showRulesModal = ref(false);
const hasAcceptedRules = ref(false);

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

const lgMarginTop = computed(() => {
	const rowHeight = window.innerWidth < 768 ? 35 : 45;
	const startFromRow = 24;
	return `${startFromRow * rowHeight}px`;
});

// Wheel zoom for desktop
const handleWheel = (event) => {
	event.preventDefault();
	const delta = event.deltaY * -0.0003;
	const newZoom = Math.max(
		isMobile.value ? 0.15 : 0.25,
		Math.min(2, zoomLevel.value + delta)
	);

	if (newZoom !== zoomLevel.value) {
		const container = event.currentTarget;
		const rect = container.getBoundingClientRect();
		const mouseX = event.clientX - rect.left;
		const mouseY = event.clientY - rect.top;

		const oldZoom = zoomLevel.value;
		zoomLevel.value = newZoom;

		const zoomRatio = newZoom / oldZoom - 1;
		panX.value -= (mouseX - rect.width / 2 - panX.value) * zoomRatio;
		panY.value -= (mouseY - rect.height / 2 - panY.value) * zoomRatio;
	}
};

// Mouse pan functions for desktop
const handleMouseDown = (event) => {
	isDragging.value = true;
	dragStart.value = {
		x: event.clientX - panX.value,
		y: event.clientY - panY.value,
	};
	event.currentTarget.style.cursor = "grabbing";
};

const handleMouseMove = (event) => {
	if (isDragging.value) {
		panX.value = event.clientX - dragStart.value.x;
		panY.value = event.clientY - dragStart.value.y;
	}
};

const handleMouseUp = (event) => {
	if (isDragging.value) {
		isDragging.value = false;
		event.currentTarget.style.cursor = "grab";
	}
};

const handleMouseLeave = (event) => {
	if (isDragging.value) {
		isDragging.value = false;
		event.currentTarget.style.cursor = "grab";
	}
};

// Touch events for mobile
const getTouchDistance = (touches) => {
	const dx = touches[0].clientX - touches[1].clientX;
	const dy = touches[0].clientY - touches[1].clientY;
	return Math.sqrt(dx * dx + dy * dy);
};

const getTouchCenter = (touches) => {
	return {
		x: (touches[0].clientX + touches[1].clientX) / 2,
		y: (touches[0].clientY + touches[1].clientY) / 2,
	};
};

const handleTouchStart = (event) => {
	if (event.touches.length === 1) {
		isDragging.value = true;
		dragStart.value = {
			x: event.touches[0].clientX - panX.value,
			y: event.touches[0].clientY - panY.value,
		};
	} else if (event.touches.length === 2) {
		event.preventDefault();
		lastTouchDistance.value = getTouchDistance(event.touches);
		lastTouchCenter.value = getTouchCenter(event.touches);
	}
};

const handleTouchMove = (event) => {
	if (event.touches.length === 1 && isDragging.value) {
		panX.value = event.touches[0].clientX - dragStart.value.x;
		panY.value = event.touches[0].clientY - dragStart.value.y;
	} else if (event.touches.length === 2) {
		event.preventDefault();
		const currentDistance = getTouchDistance(event.touches);
		const currentCenter = getTouchCenter(event.touches);

		if (lastTouchDistance.value > 0) {
			const scale = currentDistance / lastTouchDistance.value;
			const newZoom = Math.max(
				isMobile.value ? 0.15 : 0.25,
				Math.min(2, zoomLevel.value * scale)
			);

			if (newZoom !== zoomLevel.value) {
				const container = event.currentTarget;
				const rect = container.getBoundingClientRect();

				const oldZoom = zoomLevel.value;
				zoomLevel.value = newZoom;

				const zoomRatio = newZoom / oldZoom - 1;
				panX.value -=
					(currentCenter.x -
						rect.left -
						rect.width / 2 -
						panX.value) *
					zoomRatio;
				panY.value -=
					(currentCenter.y -
						rect.top -
						rect.height / 2 -
						panY.value) *
					zoomRatio;
			}
		}

		lastTouchDistance.value = currentDistance;
		lastTouchCenter.value = currentCenter;
	}
};

const handleTouchEnd = (event) => {
	if (event.touches.length === 0) {
		isDragging.value = false;
		lastTouchDistance.value = 0;
	} else if (event.touches.length === 1) {
		lastTouchDistance.value = 0;
		dragStart.value = {
			x: event.touches[0].clientX - panX.value,
			y: event.touches[0].clientY - panY.value,
		};
	}
};

// Bottom sheet handlers
const getBottomSheetTransform = () => {
	if (bottomSheetState.value === "minimized") {
		return `translateY(calc(100% - 80px + ${touchOffset.value}px))`;
	}
	if (bottomSheetState.value === "expanded") {
		return `translateY(${touchOffset.value}px)`;
	}
	return "translateY(100%)";
};

const handleBottomSheetTouchStart = (e) => {
	touchStart.value = e.touches[0].clientY;
};

const handleBottomSheetTouchMove = (e) => {
	if (touchStart.value === null) return;
	const currentTouch = e.touches[0].clientY;
	const diff = currentTouch - touchStart.value;

	if (bottomSheetState.value === "expanded" && diff > 0) {
		touchOffset.value = Math.min(diff, 100);
	} else if (bottomSheetState.value === "minimized" && diff < 0) {
		touchOffset.value = Math.max(diff, -100);
	}
};

const handleBottomSheetTouchEnd = () => {
	if (Math.abs(touchOffset.value) > 50) {
		if (touchOffset.value > 0 && bottomSheetState.value === "expanded") {
			bottomSheetState.value = "minimized";
		} else if (
			touchOffset.value < 0 &&
			bottomSheetState.value === "minimized"
		) {
			bottomSheetState.value = "expanded";
		}
	}
	touchStart.value = null;
	touchOffset.value = 0;
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
	if (tooltipTimer) {
		clearTimeout(tooltipTimer);
		tooltipTimer = null;
	}

	tooltipVisible.value = true;
	tooltipData.value = seat;

	const rect = event.target.getBoundingClientRect();
	tooltipStyle.value = {
		left: `${rect.left + rect.width / 2}px`,
		top: `${rect.top - 10}px`,
		transform: "translate(-50%, -100%)",
	};

	if (window.innerWidth < 1024) {
		tooltipTimer = setTimeout(() => {
			hideSeatTooltip();
		}, 3000);
	}
};

const hideSeatTooltip = () => {
	if (tooltipTimer) {
		clearTimeout(tooltipTimer);
		tooltipTimer = null;
	}
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

// Instructions management
const showInstructions = () => {
	instructionsClosed.value = false;
	showZoomInstructions.value = true;
};

const closeInstructions = () => {
	instructionsClosed.value = true;
	showZoomInstructions.value = false;
	localStorage.setItem("zoom_instructions_seen", "true");
};

let instructionsTimer = null;
const startInstructionsTimer = () => {
	if (instructionsTimer) clearTimeout(instructionsTimer);

	instructionsTimer = setTimeout(() => {
		if (showZoomInstructions.value) {
			closeInstructions();
		}
	}, 10000);
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

// Global touch handler
const handleGlobalTouch = (event) => {
	if (window.innerWidth >= 1024) return;

	const target = event.target;
	const isSeatButton =
		target.closest('button[class*="w-10 h-10"]') ||
		target.closest('button[class*="w-12 h-12"]');

	if (!isSeatButton && tooltipVisible.value) {
		hideSeatTooltip();
	}
};

// Zoom In Handler
const handleZoomIn = () => {
	const newZoom = Math.min(2, zoomLevel.value + 0.1);
	zoomLevel.value = newZoom;
};

// Zoom Out Handler
const handleZoomOut = () => {
	const minZoom = isMobile.value ? 0.15 : 0.25;
	const newZoom = Math.max(minZoom, zoomLevel.value - 0.1);
	zoomLevel.value = newZoom;
};

// Reset View Handler
const handleResetView = () => {
	zoomLevel.value = initialZoomLevel.value;
	panX.value = initialPanX.value;
	panY.value = initialPanY.value;
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

		document.addEventListener("touchstart", handleGlobalTouch);

		// Show zoom instructions if first time
		const hasSeenInstructions = localStorage.getItem(
			"zoom_instructions_seen"
		);
		if (!hasSeenInstructions) {
			setTimeout(() => {
				showZoomInstructions.value = true;
				startInstructionsTimer();
			}, 1500);
		} else {
			instructionsClosed.value = true;
		}
	} catch (error) {
		console.error("Failed to load:", error);
	} finally {
		loading.value = false;
	}
});

onUnmounted(() => {
	if (timer) clearInterval(timer);

	if (tooltipTimer) {
		clearTimeout(tooltipTimer);
		tooltipTimer = null;
	}

	if (instructionsTimer) {
		clearTimeout(instructionsTimer);
		instructionsTimer = null;
	}

	document.removeEventListener("touchstart", handleGlobalTouch);
});
</script>

<style scoped>
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

.no-scrollbar::-webkit-scrollbar {
	display: none;
}

.no-scrollbar {
	-ms-overflow-style: none;
	scrollbar-width: none;
}

#seat-map-container {
	-webkit-user-select: none;
	-moz-user-select: none;
	-ms-user-select: none;
	user-select: none;
	-webkit-touch-callout: none;
	overscroll-behavior: contain;
}

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

/* Zoom Instructions Animations */
.slide-up-fade-enter-active,
.slide-up-fade-leave-active {
	transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-up-fade-enter-from {
	opacity: 0;
	transform: translateY(20px);
}

.slide-up-fade-leave-to {
	opacity: 0;
	transform: translateY(10px) scale(0.95);
}

.scale-fade-enter-active,
.scale-fade-leave-active {
	transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.scale-fade-enter-from,
.scale-fade-leave-to {
	opacity: 0;
	transform: scale(0.8);
}

@keyframes float {
	0%,
	100% {
		transform: translateY(0px);
	}
	50% {
		transform: translateY(-5px);
	}
}

.fixed.bottom-6.right-6 button {
	animation: float 3s ease-in-out infinite;
}
</style>
