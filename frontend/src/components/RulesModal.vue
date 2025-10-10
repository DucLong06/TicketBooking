<template>
	<!-- Modal Overlay -->
	<Teleport to="body">
		<Transition name="modal">
			<div
				v-if="modelValue"
				class="fixed inset-0 z-[9999] overflow-y-auto"
				@click.self="handleOverlayClick"
			>
				<!-- Backdrop -->
				<div class="fixed inset-0 bg-black/70 backdrop-blur-sm"></div>

				<!-- Modal Container with proper centering -->
				<div
					class="relative min-h-screen flex items-center justify-center p-4"
				>
					<div
						class="relative bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[85vh] overflow-hidden my-8"
						@click.stop
					>
						<!-- Header -->
						<div
							class="bg-gradient-to-r from-red-600 to-orange-600 text-white px-6 py-4 flex items-center justify-between"
						>
							<div class="flex items-center space-x-3">
								<svg
									class="w-6 h-6"
									fill="none"
									stroke="currentColor"
									viewBox="0 0 24 24"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
									/>
								</svg>
								<h3 class="text-xl font-bold">
									Quy định và lưu ý quan trọng
								</h3>
							</div>
							<button
								v-if="canClose"
								@click="close"
								class="text-white/80 hover:text-white transition"
							>
								<svg
									class="w-6 h-6"
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
						</div>

						<!-- Content -->
						<div class="p-6 overflow-y-auto max-h-[60vh]">
							<!-- Venue Name -->
							<div class="mb-4 pb-4 border-b border-gray-200">
								<p class="text-sm text-gray-500">Nhà hát</p>
								<p class="text-lg font-semibold text-gray-900">
									{{ venueName }}
								</p>
							</div>

							<!-- Rules List -->
							<div class="space-y-3">
								<div
									v-for="(rule, index) in rulesList"
									:key="index"
									class="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
								>
									<div
										class="flex-shrink-0 w-6 h-6 bg-red-100 text-red-600 rounded-full flex items-center justify-center text-sm font-bold mt-0.5"
									>
										{{ index + 1 }}
									</div>
									<p class="text-gray-700 flex-1">
										{{ rule }}
									</p>
								</div>
							</div>

							<!-- Empty state -->
							<div
								v-if="rulesList.length === 0"
								class="text-center py-8 text-gray-500"
							>
								<svg
									class="w-16 h-16 mx-auto mb-4 text-gray-300"
									fill="none"
									stroke="currentColor"
									viewBox="0 0 24 24"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
									/>
								</svg>
								<p>Chưa có quy định nào được thiết lập</p>
							</div>
						</div>

						<!-- Footer with Checkbox -->
						<div
							class="bg-gray-50 px-6 py-4 border-t border-gray-200"
						>
							<label
								class="flex items-start space-x-3 cursor-pointer mb-4"
							>
								<input
									type="checkbox"
									v-model="hasReadRules"
									class="mt-1 w-5 h-5 text-red-600 border-gray-300 rounded focus:ring-red-500"
								/>
								<span class="text-sm text-gray-700">
									Tôi đã đọc và hiểu các quy định trên. Tôi
									cam kết tuân thủ các quy định của nhà hát.
								</span>
							</label>

							<div class="flex justify-end space-x-3">
								<button
									v-if="canClose"
									@click="close"
									class="px-6 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition"
								>
									Đóng
								</button>
								<button
									@click="confirm"
									:disabled="!hasReadRules"
									:class="[
										'px-6 py-2 rounded-lg font-semibold transition',
										hasReadRules
											? 'bg-gradient-to-r from-red-600 to-orange-600 text-white hover:shadow-lg'
											: 'bg-gray-300 text-gray-500 cursor-not-allowed',
									]"
								>
									{{ confirmText }}
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</Transition>
	</Teleport>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from "vue";

const props = defineProps({
	modelValue: {
		type: Boolean,
		required: true,
	},
	rules: {
		type: String,
		default: "",
	},
	venueName: {
		type: String,
		default: "Nhà hát",
	},
	canClose: {
		type: Boolean,
		default: false,
	},
	confirmText: {
		type: String,
		default: "Tôi đã hiểu",
	},
});

const emit = defineEmits(["update:modelValue", "confirm"]);

const hasReadRules = ref(false);

// Parse rules into array (split by newline)
const rulesList = computed(() => {
	if (!props.rules) return [];
	return props.rules
		.split("\n")
		.map((rule) => rule.trim())
		.filter((rule) => rule.length > 0);
});

// Lock body scroll when modal is open
watch(
	() => props.modelValue,
	(newValue) => {
		if (newValue) {
			hasReadRules.value = false;
			// Lock body scroll
			document.body.style.overflow = "hidden";
			// Scroll to top
			window.scrollTo(0, 0);
		} else {
			// Unlock body scroll
			document.body.style.overflow = "";
		}
	}
);

// Cleanup on unmount
onUnmounted(() => {
	document.body.style.overflow = "";
});

const handleOverlayClick = () => {
	if (props.canClose) {
		close();
	}
};

const close = () => {
	emit("update:modelValue", false);
};

const confirm = () => {
	if (hasReadRules.value) {
		emit("confirm");
		emit("update:modelValue", false);
	}
};
</script>

<style scoped>
/* Modal transitions */
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
	transform: scale(0.95);
}
</style>
