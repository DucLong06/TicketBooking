<template>
	<div class="markdown-wrapper">
		<div
			ref="contentRef"
			class="markdown-content prose max-w-none"
			:class="{ 'is-collapsed': isCollapsed && shouldCollapse }"
			v-html="renderedMarkdown"
		></div>

		<!-- Gradient Fade -->
		<div v-if="isCollapsed && shouldCollapse" class="fade-gradient"></div>

		<!-- Toggle Button -->
		<button
			v-if="shouldCollapse"
			@click="toggleCollapse"
			class="mt-4 text-[#d8a669] font-medium hover:text-[#b8884d] transition flex items-center gap-2"
		>
			{{ isCollapsed ? "Xem thêm" : "Thu gọn" }}
			<svg
				class="w-5 h-5 transition-transform"
				:class="{ 'rotate-180': !isCollapsed }"
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
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import { marked } from "marked";
import DOMPurify from "dompurify";

const props = defineProps({
	content: {
		type: String,
		required: true,
	},
	initialLines: {
		type: Number,
		default: 3,
	},
});

const isCollapsed = ref(true);
const shouldCollapse = ref(false);
const contentRef = ref(null);

// Configure marked
marked.setOptions({
	breaks: true,
	gfm: true,
});

const renderedMarkdown = computed(() => {
	const html = marked(props.content);
	return DOMPurify.sanitize(html);
});

const toggleCollapse = () => {
	isCollapsed.value = !isCollapsed.value;
};

onMounted(async () => {
	await nextTick();
	if (contentRef.value) {
		const lineHeight = parseInt(
			getComputedStyle(contentRef.value).lineHeight
		);
		const maxHeight = lineHeight * props.initialLines;
		shouldCollapse.value = contentRef.value.scrollHeight > maxHeight;
	}
});
</script>

<style scoped>
.markdown-wrapper {
	position: relative;
}

.markdown-content {
	transition: max-height 0.3s ease;
	overflow: hidden;
}

.markdown-content.is-collapsed {
	max-height: calc(1.5em * v-bind(initialLines));
}

.markdown-content:not(.is-collapsed) {
	max-height: none;
}

.fade-gradient {
	position: absolute;
	bottom: 2.5rem;
	left: 0;
	right: 0;
	height: 4rem;
	background: linear-gradient(to bottom, transparent, #fdfcf0);
	pointer-events: none;
}

/* Markdown Styling */
.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3) {
	color: #372e2d;
	font-weight: 700;
	margin-top: 1.5rem;
	margin-bottom: 0.75rem;
}

.markdown-content :deep(p) {
	color: #372e2d;
	line-height: 1.75;
	margin-bottom: 1rem;
}

.markdown-content :deep(img) {
	max-width: 100%;
	border-radius: 0.5rem;
	margin: 1rem 0;
}

.markdown-content :deep(a) {
	color: #d8a669;
	text-decoration: underline;
}

.markdown-content :deep(a:hover) {
	color: #b8884d;
}

.markdown-content :deep(iframe) {
	max-width: 100%;
	aspect-ratio: 16/9;
	border-radius: 0.5rem;
	margin: 1rem 0;
}
</style>
