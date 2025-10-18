<template>
	<Teleport to="body">
		<Transition name="modal">
			<div
				v-if="show"
				class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm"
				@click="handleBackdropClick"
			>
				<div class="relative w-full max-w-5xl" @click.stop>
					<!-- Close Button -->
					<button
						@click="$emit('close')"
						class="absolute -top-12 right-0 text-white hover:text-gray-300 transition"
					>
						<svg
							class="w-8 h-8"
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

					<!-- Video Container -->
					<div
						class="relative w-full bg-black rounded-lg overflow-hidden shadow-2xl"
						style="aspect-ratio: 16/9"
					>
						<iframe
							v-if="embedUrl"
							:src="embedUrl"
							frameborder="0"
							allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
							allowfullscreen
							class="absolute inset-0 w-full h-full"
						></iframe>
					</div>
				</div>
			</div>
		</Transition>
	</Teleport>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
	show: Boolean,
	trailerUrl: String,
});

const emit = defineEmits(["close"]);

const embedUrl = computed(() => {
	if (!props.trailerUrl) return "";

	// Convert YouTube URL to embed format
	const url = props.trailerUrl;
	let videoId = "";

	// Handle different YouTube URL formats
	if (url.includes("youtube.com/watch?v=")) {
		videoId = url.split("v=")[1]?.split("&")[0];
	} else if (url.includes("youtu.be/")) {
		videoId = url.split("youtu.be/")[1]?.split("?")[0];
	} else if (url.includes("youtube.com/embed/")) {
		return url + "?autoplay=1";
	}

	return videoId ? `https://www.youtube.com/embed/${videoId}?autoplay=1` : "";
});

const handleBackdropClick = () => {
	emit("close");
};
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
	transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
	opacity: 0;
}

.modal-enter-active .relative,
.modal-leave-active .relative {
	transition: transform 0.3s ease;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
	transform: scale(0.9);
}
</style>
