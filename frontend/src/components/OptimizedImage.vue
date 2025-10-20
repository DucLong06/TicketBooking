<template>
	<div class="optimized-image-wrapper" :class="wrapperClass">
		<img
			:src="currentSrc"
			:alt="alt"
			:class="[
				imageClass,
				{ 'opacity-0': !loaded, 'opacity-100': loaded },
			]"
			:loading="loading"
			:decoding="decoding"
			@load="onLoad"
			@error="onError"
		/>
		<!-- Loading skeleton - hiện khi chưa load xong -->
		<div
			v-if="!loaded && !error"
			class="skeleton-loader"
			:style="skeletonStyle"
		/>
		<!-- Error fallback -->
		<div v-if="error" class="error-placeholder" :style="skeletonStyle">
			<svg
				class="w-12 h-12 text-gray-300"
				fill="currentColor"
				viewBox="0 0 24 24"
			>
				<path d="M4 4h16v12H4V4m0 14h16v2H4v-2z" />
			</svg>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const props = defineProps({
	src: {
		type: String,
		required: true,
	},
	alt: {
		type: String,
		default: "",
	},
	width: {
		type: [Number, String],
		default: null,
	},
	height: {
		type: [Number, String],
		default: null,
	},
	aspectRatio: {
		type: String,
		default: "2/3",
	},
	loading: {
		type: String,
		default: "lazy",
		validator: (value) => ["lazy", "eager"].includes(value),
	},
	decoding: {
		type: String,
		default: "async",
		validator: (value) => ["async", "sync", "auto"].includes(value),
	},
	wrapperClass: {
		type: String,
		default: "",
	},
	imageClass: {
		type: String,
		default: "w-full h-full object-cover",
	},
});

const loaded = ref(false);
const error = ref(false);

const currentSrc = computed(() => {
	if (!props.src) return "";
	return props.src;
});

const skeletonStyle = computed(() => {
	const style = {};
	if (props.width) {
		style.width =
			typeof props.width === "number" ? `${props.width}px` : props.width;
	}
	if (props.height) {
		style.height =
			typeof props.height === "number"
				? `${props.height}px`
				: props.height;
	} else if (props.aspectRatio) {
		style.aspectRatio = props.aspectRatio;
	}
	return style;
});

const onLoad = () => {
	loaded.value = true;
};

const onError = () => {
	error.value = true;
	loaded.value = true;
};

onMounted(() => {
	if (props.loading === "eager") {
		const img = new Image();
		img.src = currentSrc.value;
	}
});
</script>

<style scoped>
.optimized-image-wrapper {
	position: relative;
	overflow: hidden;
	background: linear-gradient(to bottom, #e8dcc8, #d8a669);
}

.skeleton-loader {
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: linear-gradient(90deg, #e8dcc8 25%, #d8a669 50%, #e8dcc8 75%);
	background-size: 200% 100%;
	animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
	0% {
		background-position: -200% 0;
	}
	100% {
		background-position: 200% 0;
	}
}

.error-placeholder {
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
	background: linear-gradient(
		to bottom,
		rgba(232, 220, 200, 0.3),
		rgba(216, 166, 105, 0.3)
	);
}

img {
	transition: opacity 0.3s ease-in-out;
}

.opacity-0 {
	opacity: 0;
}

.opacity-100 {
	opacity: 1;
}
</style>
