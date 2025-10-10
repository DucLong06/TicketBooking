<template>
	<div class="selected-seats-display">
		<!-- Seat Map Visual -->
		<div v-if="displayMode === 'visual'" class="seat-visual-container">
			<div class="text-center mb-4">
				<h4 class="text-sm font-semibold text-gray-600">
					Sơ đồ ghế đã chọn
				</h4>
			</div>

			<!-- Group by Section -->
			<div
				v-for="section in groupedSeats"
				:key="section.id"
				class="section-group mb-4"
			>
				<div class="section-header mb-2">
					<span class="text-xs font-bold text-gray-600">
						{{ section.name }}
					</span>
				</div>

				<!-- Group by Row -->
				<div
					v-for="row in section.rows"
					:key="row.label"
					class="row-group mb-2"
				>
					<div class="flex items-center justify-center gap-2">
						<!-- Row Label -->
						<span
							class="row-label text-xs font-bold text-gray-600 w-8"
						>
							{{ row.label }}
						</span>

						<!-- Seats in Row -->
						<div class="seats-row flex gap-1">
							<div
								v-for="seat in row.seats"
								:key="seat.id"
								class="seat-box"
								:style="{
									backgroundColor:
										seat.price_category_color || '#10B981',
									borderColor: darkenColor(
										seat.price_category_color || '#10B981'
									),
								}"
								:title="`${seat.full_label} - ${formatPrice(
									seat.price
								)}`"
							>
								{{ seat.display_number || seat.number }}
							</div>
						</div>

						<!-- Row Label (right) -->
						<span
							class="row-label text-xs font-bold text-gray-600 w-8"
						>
							{{ row.label }}
						</span>
					</div>
				</div>
			</div>
		</div>

		<!-- List Mode -->
		<div v-else-if="displayMode === 'list'" class="seat-list-container">
			<div class="space-y-2">
				<div
					v-for="seat in seats"
					:key="seat.id"
					class="seat-item flex justify-between items-center p-2 bg-gray-50 rounded hover:bg-gray-100 transition-colors"
				>
					<div class="flex items-center gap-3">
						<!-- Color indicator -->
						<div
							class="w-4 h-4 rounded border-2 flex-shrink-0"
							:style="{
								backgroundColor:
									seat.price_category_color || '#10B981',
								borderColor: darkenColor(
									seat.price_category_color || '#10B981'
								),
							}"
						></div>

						<!-- Seat info -->
						<div>
							<span class="font-semibold text-gray-800">
								{{ seat.full_label }}
							</span>
							<span class="text-xs text-gray-500 ml-2">
								{{ seat.section_name }}
							</span>
						</div>
					</div>

					<!-- Price -->
					<span class="font-semibold text-gray-700">
						{{ formatPrice(seat.price) }}
					</span>
				</div>
			</div>
		</div>

		<!-- Compact Mode (like SelectSeats summary) -->
		<div
			v-else-if="displayMode === 'compact'"
			class="seat-compact-container"
		>
			<div class="flex flex-wrap gap-2">
				<div
					v-for="seat in seats"
					:key="seat.id"
					class="seat-badge"
					:style="{
						backgroundColor: seat.price_category_color || '#10B981',
						borderColor: darkenColor(
							seat.price_category_color || '#10B981'
						),
					}"
				>
					<span class="font-semibold text-white text-sm">
						{{ seat.full_label }}
					</span>
				</div>
			</div>
		</div>

		<!-- Total Summary -->
		<div v-if="showSummary" class="summary-section mt-4 pt-4 border-t">
			<div class="flex justify-between items-center">
				<div>
					<span class="text-sm text-gray-600">Tổng số ghế:</span>
					<span class="ml-2 font-semibold">{{ seats.length }}</span>
				</div>
				<div>
					<span class="text-sm text-gray-600">Tổng tiền:</span>
					<span class="ml-2 text-lg font-bold text-primary-600">
						{{ formatPrice(totalAmount) }}
					</span>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
	seats: {
		type: Array,
		required: true,
		default: () => [],
	},
	displayMode: {
		type: String,
		default: "visual", // 'visual' | 'list' | 'compact'
		validator: (value) => ["visual", "list", "compact"].includes(value),
	},
	showSummary: {
		type: Boolean,
		default: true,
	},
});

// Group seats by section and row for visual display
const groupedSeats = computed(() => {
	const sections = {};

	props.seats.forEach((seat) => {
		const sectionId = seat.section_id || "main";
		const sectionName = seat.section_name || "Khán phòng chính";

		if (!sections[sectionId]) {
			sections[sectionId] = {
				id: sectionId,
				name: sectionName,
				rows: {},
			};
		}

		const rowLabel = seat.row;
		if (!sections[sectionId].rows[rowLabel]) {
			sections[sectionId].rows[rowLabel] = {
				label: rowLabel,
				seats: [],
			};
		}

		sections[sectionId].rows[rowLabel].seats.push(seat);
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
	return props.seats.reduce((sum, seat) => sum + (seat.price || 0), 0);
});

// Helper functions
const formatPrice = (price) => {
	return new Intl.NumberFormat("vi-VN", {
		style: "currency",
		currency: "VND",
	}).format(price || 0);
};

const darkenColor = (color) => {
	// Simple color darkening for border
	if (!color) return "#059669";

	// Remove # if present
	color = color.replace("#", "");

	// Convert to RGB
	const r = parseInt(color.substr(0, 2), 16);
	const g = parseInt(color.substr(2, 2), 16);
	const b = parseInt(color.substr(4, 2), 16);

	// Darken by 20%
	const darken = (val) => Math.max(0, Math.floor(val * 0.8));

	const newR = darken(r).toString(16).padStart(2, "0");
	const newG = darken(g).toString(16).padStart(2, "0");
	const newB = darken(b).toString(16).padStart(2, "0");

	return `#${newR}${newG}${newB}`;
};
</script>

<style scoped>
.selected-seats-display {
	width: 100%;
}

.seat-visual-container {
	padding: 1rem;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	border-radius: 12px;
}

.section-group {
	background: rgba(255, 255, 255, 0.95);
	padding: 0.75rem;
	border-radius: 8px;
}

.section-header {
	text-align: center;
	padding-bottom: 0.5rem;
	border-bottom: 2px solid #e5e7eb;
}

.row-group {
	display: flex;
	justify-content: center;
}

.row-label {
	text-align: center;
	display: inline-block;
}

.seats-row {
	display: flex;
	flex-wrap: wrap;
	justify-content: center;
	max-width: 600px;
}

.seat-box {
	width: 32px;
	height: 32px;
	display: flex;
	align-items: center;
	justify-content: center;
	border-radius: 6px;
	border: 2px solid;
	color: white;
	font-size: 11px;
	font-weight: 600;
	cursor: default;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	transition: transform 0.2s;
}

.seat-box:hover {
	transform: scale(1.1);
}

.seat-list-container {
	max-height: 300px;
	overflow-y: auto;
}

.seat-item {
	border: 1px solid #e5e7eb;
}

.seat-compact-container {
	padding: 0.5rem;
}

.seat-badge {
	padding: 0.5rem 1rem;
	border-radius: 8px;
	border: 2px solid;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.summary-section {
	background: #f9fafb;
	padding: 1rem;
	border-radius: 8px;
}

/* Scrollbar styling */
.seat-list-container::-webkit-scrollbar {
	width: 6px;
}

.seat-list-container::-webkit-scrollbar-track {
	background: #f1f1f1;
	border-radius: 10px;
}

.seat-list-container::-webkit-scrollbar-thumb {
	background: #888;
	border-radius: 10px;
}

.seat-list-container::-webkit-scrollbar-thumb:hover {
	background: #555;
}
</style>
