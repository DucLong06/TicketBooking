<template>
	<footer class="bg-gray-800 text-white mt-auto">
		<div class="container mx-auto px-4 py-8">
			<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
				<!-- Contact Info -->
				<div>
					<h3 class="text-lg font-semibold mb-4">Liên hệ</h3>
					<p
						class="text-gray-300"
						v-if="contactInfo?.hotline_display"
					>
						📞 {{ contactInfo.hotline_display }}
					</p>
					<p class="text-gray-300" v-if="contactInfo?.support_email">
						✉️ {{ contactInfo.support_email }}
					</p>
				</div>

				<!-- Quick Links -->
				<div>
					<h3 class="text-lg font-semibold mb-4">Liên kết nhanh</h3>
					<ul class="space-y-2 text-gray-300">
						<li>
							<a href="/" class="hover:text-white transition">
								Trang chủ
							</a>
						</li>
						<li>
							<a
								href="/#shows"
								class="hover:text-white transition"
							>
								Lịch diễn
							</a>
						</li>
						<li>
							<a
								href="/#about"
								class="hover:text-white transition"
							>
								Giới thiệu
							</a>
						</li>
					</ul>
				</div>

				<!-- Social -->
				<div>
					<h3 class="text-lg font-semibold mb-4">
						Theo dõi chúng tôi
					</h3>
					<div class="flex space-x-4">
						<a
							v-if="contactInfo?.facebook_url"
							:href="contactInfo.facebook_url"
							target="_blank"
							rel="noopener noreferrer"
							class="text-gray-300 hover:text-white transition"
						>
							Facebook
						</a>
						<a
							v-if="contactInfo?.instagram_url"
							:href="contactInfo.instagram_url"
							target="_blank"
							rel="noopener noreferrer"
							class="text-gray-300 hover:text-white transition"
						>
							Instagram
						</a>
						<a
							v-if="contactInfo?.tiktok_url"
							:href="contactInfo.tiktok_url"
							target="_blank"
							rel="noopener noreferrer"
							class="text-gray-300 hover:text-white transition"
						>
							TikTok
						</a>
					</div>
				</div>
			</div>

			<div
				class="border-t border-gray-700 mt-8 pt-4 text-center text-gray-400"
			>
				<p>
					&copy;
					{{ contactInfo?.copyright_text || "Theater Booking" }}
				</p>
			</div>
		</div>
	</footer>
</template>

<script setup>
import { onMounted } from "vue";
import { useContact } from "@/composables/useContact";

const { contactInfo, fetchContactInfo } = useContact();

onMounted(async () => {
	await fetchContactInfo();
});
</script>
