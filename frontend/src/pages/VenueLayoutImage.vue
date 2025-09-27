<template>
	<div class="venue-layout-preview">
		<svg
			v-if="venueType === 'opera'"
			width="400"
			height="300"
			viewBox="0 0 400 300"
			class="border rounded-lg bg-gray-50"
		>
			<!-- Stage -->
			<rect
				x="150"
				y="10"
				width="100"
				height="15"
				fill="#4B5563"
				rx="5"
			/>
			<text
				x="200"
				y="22"
				text-anchor="middle"
				class="text-xs fill-white"
			>
				SÂN KHẤU
			</text>

			<!-- Tầng 1 chính -->
			<g>
				<!-- VIP rows A-G (cam) -->
				<rect
					x="50"
					y="40"
					width="300"
					height="80"
					fill="#FF6B35"
					opacity="0.3"
					rx="5"
				/>
				<text x="200" y="55" text-anchor="middle" class="text-xs">
					Tầng 1 chính
				</text>
				<text x="200" y="70" text-anchor="middle" class="text-xs">
					A-G (VIP)
				</text>
				<text x="200" y="85" text-anchor="middle" class="text-xs">
					H-I (Standard)
				</text>

				<!-- LG boxes -->
				<rect
					x="20"
					y="60"
					width="20"
					height="40"
					fill="#9B59B6"
					opacity="0.5"
					rx="3"
				/>
				<text x="30" y="82" text-anchor="middle" class="text-xs">
					LG
				</text>

				<rect
					x="360"
					y="60"
					width="20"
					height="40"
					fill="#9B59B6"
					opacity="0.5"
					rx="3"
				/>
				<text x="370" y="82" text-anchor="middle" class="text-xs">
					LG
				</text>
			</g>

			<!-- Tầng trên -->
			<g>
				<!-- Upper AA-CC (xanh lá) -->
				<rect
					x="80"
					y="140"
					width="240"
					height="30"
					fill="#06A77D"
					opacity="0.3"
					rx="5"
				/>
				<text x="200" y="158" text-anchor="middle" class="text-xs">
					Tầng trên: AA-CC
				</text>

				<!-- Main floor 2 A-I (xanh dương + economy) -->
				<rect
					x="60"
					y="180"
					width="280"
					height="60"
					fill="#3498DB"
					opacity="0.3"
					rx="5"
				/>
				<text x="200" y="198" text-anchor="middle" class="text-xs">
					A-F (Balcony)
				</text>
				<text x="200" y="213" text-anchor="middle" class="text-xs">
					G-I (Economy)
				</text>
			</g>

			<!-- Legend -->
			<g transform="translate(10, 260)">
				<circle cx="8" cy="8" r="4" fill="#FF6B35" />
				<text x="16" y="12" class="text-xs">VIP</text>

				<circle cx="60" cy="8" r="4" fill="#FFD23F" />
				<text x="68" y="12" class="text-xs">Standard</text>

				<circle cx="130" cy="8" r="4" fill="#06A77D" />
				<text x="138" y="12" class="text-xs">Upper</text>

				<circle cx="180" cy="8" r="4" fill="#3498DB" />
				<text x="188" y="12" class="text-xs">Balcony</text>

				<circle cx="240" cy="8" r="4" fill="#E67E22" />
				<text x="248" y="12" class="text-xs">Economy</text>

				<circle cx="300" cy="8" r="4" fill="#9B59B6" />
				<text x="308" y="12" class="text-xs">Loge</text>
			</g>
		</svg>

		<!-- Placeholder cho venue khác -->
		<div
			v-else
			class="w-full h-48 bg-gray-100 border rounded-lg flex items-center justify-center"
		>
			<div class="text-center text-gray-500">
				<div class="text-lg font-semibold">{{ venueName }}</div>
				<div class="text-sm">Sơ đồ nhà hát</div>
			</div>
		</div>
	</div>
</template>

<script setup>
const props = defineProps({
	venueType: {
		type: String,
		default: "theater",
	},
	venueName: {
		type: String,
		default: "Nhà hát",
	},
});
</script>
