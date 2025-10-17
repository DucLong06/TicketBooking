<template>
	<header class="bg-black shadow-md top-0">
		<div class="container mx-auto px-4">
			<div class="flex items-center justify-between h-16">
				<!-- Logo -->
				<div class="flex items-center space-x-3">
					<img
						class="h-12 w-auto object-contain"
						src="/logo_DCART-1.png"
						alt="Dương Cầm ART Logo"
					/>
				</div>

				<!-- Desktop Navigation -->
				<nav class="hidden md:flex items-center space-x-8">
					<a
						href="/"
						class="text-white hover:text-primary-600 transition font-medium"
					>
						Trang chủ
					</a>
					<a
						href="/lookup"
						class="text-white hover:text-primary-600 transition font-medium"
					>
						Tra cứu vé
					</a>
					<a
						href="/https://www.giacmochipheo.com.vn/"
						class="text-white hover:text-primary-600 transition font-medium"
					>
						Về chúng tôi
					</a>
					<a
						v-if="contactInfo?.hotline_display"
						:href="`tel:${contactInfo.hotline}`"
						class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition font-medium"
					>
						📞 {{ contactInfo.hotline_display }}
					</a>
				</nav>

				<!-- Mobile menu button -->
				<button
					@click="toggleMenu"
					class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition"
					aria-label="Toggle menu"
				>
					<svg
						class="w-6 h-6 text-gray-700"
						fill="none"
						stroke="currentColor"
						:class="{ hidden: isMenuOpen }"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M4 6h16M4 12h16M4 18h16"
						/>
					</svg>
					<svg
						class="w-6 h-6 text-gray-700"
						fill="none"
						stroke="currentColor"
						:class="{ hidden: !isMenuOpen }"
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

			<!-- Mobile Navigation Menu -->
			<Transition
				enter-active-class="transition ease-out duration-200"
				enter-from-class="opacity-0 -translate-y-2"
				enter-to-class="opacity-100 translate-y-0"
				leave-active-class="transition ease-in duration-150"
				leave-from-class="opacity-100 translate-y-0"
				leave-to-class="opacity-0 -translate-y-2"
			>
				<nav
					v-show="isMenuOpen"
					class="md:hidden py-4 border-t border-gray-200"
				>
					<div class="flex flex-col space-y-3">
						<a
							href="/"
							@click="closeMenu"
							class="text-gray-700 hover:text-primary-600 hover:bg-gray-50 px-4 py-3 rounded-lg transition font-medium"
						>
							🏠 Trang chủ
						</a>
						<a
							href="/lookup"
							@click="closeMenu"
							class="text-gray-700 hover:text-primary-600 hover:bg-gray-50 px-4 py-3 rounded-lg transition font-medium"
						>
							🔍 Tra cứu vé
						</a>
						<a
							href="/https://www.giacmochipheo.com.vn/"
							@click="closeMenu"
							class="text-gray-700 hover:text-primary-600 hover:bg-gray-50 px-4 py-3 rounded-lg transition font-medium"
						>
							ℹ️ Về chúng tôi
						</a>
						<a
							v-if="contactInfo?.hotline_display"
							:href="`tel:${contactInfo.hotline}`"
							@click="closeMenu"
							class="bg-primary-600 text-white px-4 py-3 rounded-lg hover:bg-primary-700 transition font-medium text-center"
						>
							📞 Hotline: {{ contactInfo.hotline_display }}
						</a>
						<div
							v-if="contactInfo"
							class="flex justify-center space-x-4 pt-2 border-t border-gray-200"
						>
							<a
								v-if="contactInfo.facebook_url"
								:href="contactInfo.facebook_url"
								target="_blank"
								rel="noopener noreferrer"
								class="text-gray-600 hover:text-primary-600 transition"
								aria-label="Facebook"
							>
								<svg
									class="w-6 h-6"
									fill="currentColor"
									viewBox="0 0 24 24"
								>
									<path
										d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"
									/>
								</svg>
							</a>
							<a
								v-if="contactInfo.tiktok_url"
								:href="contactInfo.tiktok_url"
								target="_blank"
								rel="noopener noreferrer"
								class="text-gray-600 hover:text-primary-600 transition"
								aria-label="TikTok"
							>
								<svg
									class="w-6 h-6"
									fill="currentColor"
									viewBox="0 0 24 24"
								>
									<path
										d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"
									/>
								</svg>
							</a>
							<a
								v-if="contactInfo.instagram_url"
								:href="contactInfo.instagram_url"
								target="_blank"
								rel="noopener noreferrer"
								class="text-gray-600 hover:text-primary-600 transition"
								aria-label="Instagram"
							>
								<svg
									class="w-6 h-6"
									fill="currentColor"
									viewBox="0 0 24 24"
								>
									<path
										d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"
									/>
								</svg>
							</a>
						</div>
					</div>
				</nav>
			</Transition>
		</div>
	</header>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useContact } from "@/composables/useContact";

const { contactInfo, fetchContactInfo } = useContact();
const isMenuOpen = ref(false);

const toggleMenu = () => {
	isMenuOpen.value = !isMenuOpen.value;
};

const closeMenu = () => {
	isMenuOpen.value = false;
};

onMounted(async () => {
	await fetchContactInfo();
});
</script>
