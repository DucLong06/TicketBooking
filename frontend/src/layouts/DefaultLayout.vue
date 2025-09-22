<template>
	<div class="min-h-screen flex flex-col bg-gray-50">
		<AppHeader />

		<main class="flex-grow">
			<slot />
		</main>

		<AppFooter />
	</div>
</template>

<script setup>
import AppHeader from "@/components/common/AppHeader.vue";
import AppFooter from "@/components/common/AppFooter.vue";
</script>
