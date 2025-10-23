<template>
	<div class="min-h-screen flex flex-col bg-gray-50">
		<AppHeader />

		<main class="flex-grow bg-[#fdfcf0]">
			<slot />
		</main>

		<AppFooter />
		<FloatingContacts />
	</div>
</template>

<script setup>
import AppHeader from "@/components/common/AppHeader.vue";
import AppFooter from "@/components/common/AppFooter.vue";
import FloatingContacts from "@/components/FloatingContacts.vue";
</script>
