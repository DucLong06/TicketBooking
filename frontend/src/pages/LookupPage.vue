<template>
	<DefaultLayout>
		<div class="container mx-auto px-4 py-8">
			<h1 class="text-3xl font-bold text-center mb-8 text-[#372e2d]">
				Tra Cứu Thông Tin Vé
			</h1>

			<!-- Search Form -->
			<div
				class="max-w-xl mx-auto bg-[#fdfcf0] border-2 border-[#d8a669] p-6 rounded-lg shadow-md mb-8"
			>
				<form @submit.prevent="handleSearch">
					<div
						class="flex items-center border-b-2 border-[#d8a669] py-2"
					>
						<input
							v-model="searchQuery"
							class="appearance-none bg-transparent border-none w-full text-[#372e2d] mr-3 py-1 px-2 leading-tight focus:outline-none placeholder-[#372e2d]/50"
							type="text"
							placeholder="Nhập mã vé hoặc SĐT"
							aria-label="Search query"
						/>
						<button
							class="flex-shrink-0 bg-[#d8a669] hover:bg-[#b8884d] text-sm text-white font-bold py-2 px-6 rounded-lg transition-all hover:shadow-lg transform hover:scale-105 active:scale-95"
							type="submit"
							:disabled="isLoading"
						>
							<span v-if="!isLoading">Tra cứu</span>
							<span v-else>Đang tìm...</span>
						</button>
					</div>
				</form>
			</div>

			<!-- Loading State -->
			<div v-if="isLoading" class="text-center py-8">
				<DuongCamLoading size="lg" message="Đang tải thông tin..." />
			</div>

			<!-- Error Message -->
			<div
				v-if="error"
				class="max-w-xl mx-auto bg-red-100 border-2 border-red-400 text-red-700 px-4 py-3 rounded-lg relative"
				role="alert"
			>
				<strong class="font-bold">Lỗi!</strong>
				<span class="block sm:inline">{{ error }}</span>
			</div>

			<!-- No Results Message -->
			<div
				v-if="searched && bookings.length === 0 && !isLoading && !error"
				class="text-center text-[#372e2d]/70"
			>
				<p class="text-lg font-medium">
					Không tìm thấy vé nào phù hợp với thông tin bạn cung cấp.
				</p>
				<p class="text-sm mt-2">
					Vui lòng kiểm tra lại mã vé hoặc số điện thoại.
				</p>
			</div>

			<!-- Results -->
			<div v-if="bookings.length > 0" class="space-y-6 max-w-4xl mx-auto">
				<div
					v-for="booking in bookings"
					:key="booking.id"
					class="bg-[#fdfcf0] border-2 border-[#d8a669] rounded-lg shadow-lg overflow-hidden"
				>
					<div class="p-6">
						<div class="flex justify-between items-start mb-4">
							<div>
								<h2 class="text-2xl font-bold text-[#372e2d]">
									{{ booking.show_name }}
								</h2>
								<p class="text-sm text-[#372e2d]/70 mt-1">
									Mã vé:
									<span
										class="font-semibold text-[#d8a669]"
										>{{ booking.booking_code }}</span
									>
								</p>
							</div>
							<span
								class="text-sm font-semibold px-3 py-1 rounded-full"
								:class="{
									'bg-green-100 text-green-800 border border-green-300':
										booking.status === 'paid',
									'bg-yellow-100 text-yellow-800 border border-yellow-300':
										booking.status === 'pending',
									'bg-red-100 text-red-800 border border-red-300':
										booking.status === 'cancelled',
								}"
							>
								{{
									booking.status === "paid"
										? "Đã thanh toán"
										: "Chưa thanh toán"
								}}
							</span>
						</div>

						<div
							class="mt-4 border-t border-[#d8a669]/30 pt-4 space-y-3"
						>
							<div class="flex justify-between">
								<span class="text-[#372e2d]/70"
									>Ngày diễn:</span
								>
								<span class="font-medium text-[#372e2d]">{{
									new Date(
										booking.performance_datetime
									).toLocaleDateString("vi-VN")
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-[#372e2d]/70">Giờ diễn:</span>
								<span class="font-medium text-[#372e2d]">{{
									new Date(
										booking.performance_datetime
									).toLocaleTimeString("vi-VN", {
										hour: "2-digit",
										minute: "2-digit",
									})
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-[#372e2d]/70">Địa điểm:</span>
								<span
									class="font-medium text-right text-[#372e2d]"
									>{{ booking.venue_name }}</span
								>
							</div>
							<div class="flex justify-between items-start">
								<span class="text-[#372e2d]/70">Ghế:</span>
								<div class="text-right">
									<span
										v-for="seat in booking.seat_reservations"
										:key="seat.id"
										class="block font-medium text-[#372e2d]"
									>
										{{ seat.seat_label }} -
										{{ seat.section_name }}
									</span>
								</div>
							</div>
							<div
								class="flex justify-between pt-3 border-t border-[#d8a669]/30"
							>
								<span class="text-[#372e2d] font-semibold"
									>Tổng tiền:</span
								>
								<span
									class="font-bold text-xl text-[#d8a669]"
									>{{
										formatPrice(booking.final_amount)
									}}</span
								>
							</div>
						</div>

						<div class="mt-6 text-right">
							<button
								@click="resendEmail(booking.booking_code)"
								:disabled="
									resendingEmailCode === booking.booking_code
								"
								class="bg-[#d8a669] hover:bg-[#b8884d] text-white font-bold py-2 px-6 rounded-lg transition-all hover:shadow-lg transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
							>
								<span
									v-if="
										resendingEmailCode ===
										booking.booking_code
									"
									>Đang gửi...</span
								>
								<span v-else>Gửi lại Email</span>
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	</DefaultLayout>
</template>
<script setup>
import { ref } from "vue";
import DefaultLayout from "../layouts/DefaultLayout.vue";
import { bookingAPI } from "../api/booking";
import { useToast } from "vue-toastification";
import DuongCamLoading from "@/components/common/DuongCamLoading.vue";

const toast = useToast();
const searchQuery = ref("");
const bookings = ref([]);
const isLoading = ref(false);
const error = ref(null);
const searched = ref(false);
const resendingEmailCode = ref(null);

const handleSearch = async () => {
	if (!searchQuery.value.trim()) {
		toast.warning("Vui lòng nhập mã vé hoặc số điện thoại.");
		return;
	}
	isLoading.value = true;
	error.value = null;
	searched.value = true;
	bookings.value = [];

	try {
		const response = await bookingAPI.searchBookings(searchQuery.value);
		bookings.value = response.data;
		if (bookings.value.length === 0) {
			toast.info("Không tìm thấy thông tin đặt vé phù hợp.");
		}
	} catch (e) {
		error.value = "Đã xảy ra lỗi khi tra cứu. Vui lòng thử lại.";
		toast.error(error.value);
	} finally {
		isLoading.value = false;
	}
};

const resendEmail = async (bookingCode) => {
	resendingEmailCode.value = bookingCode;
	try {
		const response = await bookingAPI.resendEmail(bookingCode);
		if (response.data.success) {
			toast.success(
				response.data.message || "Email đã được gửi lại thành công!"
			);
		} else {
			toast.error(response.data.error || "Gửi email thất bại.");
		}
	} catch (e) {
		toast.error("Có lỗi xảy ra khi gửi lại email.");
	} finally {
		resendingEmailCode.value = null;
	}
};

const formatPrice = (price) => {
	return new Intl.NumberFormat("vi-VN", {
		style: "currency",
		currency: "VND",
	}).format(price);
};
</script>
