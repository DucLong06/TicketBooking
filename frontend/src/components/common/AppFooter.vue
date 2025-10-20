<template>
	<footer class="bg-[#372e2d] text-[#d8a669] mt-auto">
		<div class="container mx-auto px-4 py-8">
			<div class="grid grid-cols-1 md:grid-cols-4 gap-8">
				<!-- Contact Info -->
				<div>
					<h3 class="text-lg font-semibold mb-4">Liên hệ</h3>
					<p
						class="text-[#d8a669]"
						v-if="contactInfo?.hotline_display"
					>
						📞 {{ contactInfo.hotline_display }}
					</p>
					<p class="text-[#d8a669]" v-if="contactInfo?.support_email">
						✉️ {{ contactInfo.support_email }}
					</p>
				</div>

				<!-- Quick Links -->
				<div>
					<h3 class="text-lg font-semibold mb-4">Liên kết nhanh</h3>
					<ul class="space-y-2 text-[#d8a669]">
						<li>
							<a href="/" class="hover:text-[#d8a669] transition">
								Trang chủ
							</a>
						</li>

						<li>
							<a
								href="https://duongcam.art/"
								class="hover:text-[#d8a669] transition"
							>
								Giới thiệu
							</a>
						</li>
					</ul>
				</div>

				<!-- Terms & Policies -->
				<div>
					<h3 class="text-lg font-semibold mb-4">
						Điều khoản sử dụng
					</h3>
					<ul class="space-y-2 text-[#d8a669]">
						<li>
							<a
								href="/terms/GeneralTerms.html"
								class="hover:text-[#d8a669] transition"
							>
								Điều Kiện Giao Dịch Chung
							</a>
						</li>
						<li>
							<a
								href="/terms/GeneralTerms.html"
								class="hover:text-[#d8a669] transition"
							>
								Chính Sách Bảo Mật Thông Tin
							</a>
						</li>
						<li>
							<a
								href="/terms/GeneralTerms.html"
								class="hover:text-[#d8a669] transition"
							>
								Chính Sách Giao Nhận
							</a>
						</li>
						<li>
							<a
								href="/terms/GeneralTerms.html"
								class="hover:text-[#d8a669] transition"
							>
								Chính Sách Đặt Chỗ Và Thanh Toán
							</a>
						</li>
						<!-- <li>
							<a
								href="/terms/GeneralTerms.html"
								class="hover:text-[#d8a669] transition"
							>
								Câu Hỏi Thường Gặp
							</a>
						</li> -->
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
							class="text-[#d8a669] hover:text-[#d8a669] transition"
						>
							Facebook
						</a>
						<a
							v-if="contactInfo?.instagram_url"
							:href="contactInfo.instagram_url"
							target="_blank"
							rel="noopener noreferrer"
							class="text-[#d8a669] hover:text-[#d8a669] transition"
						>
							Instagram
						</a>
						<a
							v-if="contactInfo?.tiktok_url"
							:href="contactInfo.tiktok_url"
							target="_blank"
							rel="noopener noreferrer"
							class="text-[#d8a669] hover:text-[#d8a669] transition"
						>
							TikTok
						</a>
					</div>
				</div>
			</div>
			<div class="border-t border-[#4a3f3e] mt-8 pt-4 text-gray-400">
				<div class="">
					<div class="flex flex-col space-y-2 text-sm">
						<p>
							© 2025 Công ty TNHH Phát triển nghệ thuật và giải
							trí Dương Cầm
						</p>
						<p>
							GPĐKKD: 0106683236 do Phòng ĐKKD- Sở KH&ĐT TP Hà Nội
							cấp ngày 04/11/2014.
						</p>
						<p>
							Địa chỉ: Số nhà 11, Ngõ 86, phố Hào Nam, Phường Ô
							Chợ Dừa, Thành phố Hà Nội, Việt Nam.
						</p>
						<p>
							Hotline: 0962.98.98.56 | Email: support@duongcam.art
						</p>
					</div>
				</div>
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
