<template>
	<div class="duong-cam-loading" :class="sizeClass">
		<!-- Three animated dots inspired by logo -->
		<div class="loading-dots">
			<div class="dot dot-1"></div>
			<div class="dot dot-2"></div>
			<div class="dot dot-3"></div>
		</div>

		<div v-if="showBranding" class="loading-branding">
			{{ brandingText }}
		</div>

		<!-- Loading message -->
		<div v-if="message" class="loading-message">
			{{ message }}
		</div>
	</div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
	size: {
		type: String,
		default: "md",
		validator: (value) => ["sm", "md", "lg", "xl"].includes(value),
	},
	showBranding: {
		type: Boolean,
		default: true,
	},
	brandingText: {
		type: String,
		default: "Duong Cam Art",
	},
	message: {
		type: String,
		default: "",
	},
});

const sizeClass = computed(() => `loading-size-${props.size}`);
</script>

<style scoped>
.duong-cam-loading {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	gap: 1rem;
}

/* Three dots container */
.loading-dots {
	display: flex;
	align-items: center;
	gap: 0.5rem;
}

/* Individual dot with gradient like logo */
.dot {
	border-radius: 50%;
	animation: bounce 1.4s ease-in-out infinite;
}

/* Gradient colors matching logo */
.dot-1 {
	background: linear-gradient(135deg, #e91e63 0%, #f44336 100%);
	animation-delay: 0s;
}

.dot-2 {
	background: linear-gradient(135deg, #f44336 0%, #ff5722 100%);
	animation-delay: 0.2s;
}

.dot-3 {
	background: linear-gradient(135deg, #ff5722 0%, #ff9800 100%);
	animation-delay: 0.4s;
}

/* Branding text */
.loading-branding {
	font-family: "Georgia", serif;
	font-weight: 600;
	letter-spacing: 1px;
	color: #372e2d;
	text-transform: uppercase;
	background: linear-gradient(135deg, #e91e63 0%, #ff5722 50%, #ff9800 100%);
	-webkit-background-clip: text;
	-webkit-text-fill-color: transparent;
	background-clip: text;
	animation: shimmer 2s ease-in-out infinite;
}

/* Loading message */
.loading-message {
	color: #6b5e5d;
	text-align: center;
	animation: fade 1.5s ease-in-out infinite;
}

/* Size variants for dots */
.loading-size-sm .dot {
	width: 8px;
	height: 8px;
}

.loading-size-sm .loading-dots {
	gap: 0.375rem;
}

.loading-size-sm .loading-branding {
	font-size: 0.75rem;
}

.loading-size-sm .loading-message {
	font-size: 0.75rem;
}

.loading-size-md .dot {
	width: 12px;
	height: 12px;
}

.loading-size-md .loading-dots {
	gap: 0.5rem;
}

.loading-size-md .loading-branding {
	font-size: 0.875rem;
}

.loading-size-md .loading-message {
	font-size: 0.875rem;
}

.loading-size-lg .dot {
	width: 16px;
	height: 16px;
}

.loading-size-lg .loading-dots {
	gap: 0.625rem;
}

.loading-size-lg .loading-branding {
	font-size: 1rem;
}

.loading-size-lg .loading-message {
	font-size: 0.875rem;
}

.loading-size-xl .dot {
	width: 20px;
	height: 20px;
}

.loading-size-xl .loading-dots {
	gap: 0.75rem;
}

.loading-size-xl .loading-branding {
	font-size: 1.25rem;
}

.loading-size-xl .loading-message {
	font-size: 1rem;
}

/* Animations */
@keyframes bounce {
	0%,
	80%,
	100% {
		transform: translateY(0) scale(1);
		opacity: 1;
	}
	40% {
		transform: translateY(-20px) scale(1.1);
		opacity: 0.8;
	}
}

@keyframes shimmer {
	0%,
	100% {
		opacity: 1;
	}
	50% {
		opacity: 0.7;
	}
}

@keyframes fade {
	0%,
	100% {
		opacity: 0.5;
	}
	50% {
		opacity: 1;
	}
}

/* Mobile optimizations */
@media (max-width: 640px) {
	.loading-size-md .dot {
		width: 10px;
		height: 10px;
	}

	.loading-size-lg .dot {
		width: 14px;
		height: 14px;
	}

	.loading-size-xl .dot {
		width: 18px;
		height: 18px;
	}

	.loading-dots {
		gap: 0.5rem;
	}
}
</style>
