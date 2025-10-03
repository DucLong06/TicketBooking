<template>
	<DefaultLayout>
		<div class="container mx-auto px-4 py-8">
			<h1 class="text-3xl font-bold text-center mb-8">
				Tra Cứu Thông Tin Vé
			</h1>

			<!-- Search Form -->
			<div
				class="max-w-xl mx-auto bg-white p-6 rounded-lg shadow-md mb-8"
			>
				<form @submit.prevent="handleSearch">
					<div
						class="flex items-center border-b-2 border-primary-500 py-2"
					>
						<input
							v-model="searchQuery"
							class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none"
							type="text"
							placeholder="Nhập mã vé hoặc SĐT"
							aria-label="Search query"
						/>
						<button
							class="flex-shrink-0 bg-primary-600 hover:bg-primary-700 border-primary-600 hover:border-primary-700 text-sm border-4 text-white py-1 px-4 rounded"
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
			<div v-if="isLoading" class="text-center">
				<div
					class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"
				></div>
				<p class="mt-2 text-gray-600">Đang tải thông tin...</p>
			</div>

			<!-- Error Message -->
			<div
				v-if="error"
				class="max-w-xl mx-auto bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
				role="alert"
			>
				<strong class="font-bold">Lỗi!</strong>
				<span class="block sm:inline">{{ error }}</span>
			</div>

			<!-- No Results Message -->
			<div
				v-if="searched && bookings.length === 0 && !isLoading && !error"
				class="text-center text-gray-500"
			>
				<p>Không tìm thấy vé nào phù hợp với thông tin bạn cung cấp.</p>
				<p class="text-sm">
					Vui lòng kiểm tra lại mã vé hoặc số điện thoại.
				</p>
			</div>

			<!-- Results -->
			<div v-if="bookings.length > 0" class="space-y-6 max-w-4xl mx-auto">
				<div
					v-for="booking in bookings"
					:key="booking.id"
					class="bg-white rounded-lg shadow-lg overflow-hidden"
				>
					<div class="p-6">
						<div class="flex justify-between items-start">
							<div>
								<h2 class="text-2xl font-bold text-primary-700">
									{{ booking.show_name }}
								</h2>
								<p class="text-sm text-gray-500">
									Mã vé:
									<span class="font-semibold text-gray-800">{{
										booking.booking_code
									}}</span>
								</p>
							</div>
							<span
								class="text-sm font-semibold px-3 py-1 rounded-full"
								:class="{
									'bg-green-100 text-green-800':
										booking.status === 'paid',
									'bg-yellow-100 text-yellow-800':
										booking.status === 'pending',
									'bg-red-100 text-red-800':
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

						<div class="mt-4 border-t pt-4 space-y-3">
							<div class="flex justify-between">
								<span class="text-gray-600">Ngày diễn:</span>
								<span class="font-medium">{{
									new Date(
										booking.performance_datetime
									).toLocaleDateString("vi-VN")
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">Giờ diễn:</span>
								<span class="font-medium">{{
									new Date(
										booking.performance_datetime
									).toLocaleTimeString("vi-VN", {
										hour: "2-digit",
										minute: "2-digit",
									})
								}}</span>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">Địa điểm:</span>
								<span class="font-medium text-right">{{
									booking.venue_name
								}}</span>
							</div>
							<div class="flex justify-between items-start">
								<span class="text-gray-600">Ghế:</span>
								<div class="text-right">
									<span
										v-for="seat in booking.seat_reservations"
										:key="seat.id"
										class="block font-medium"
									>
										{{ seat.seat_label }} -
										{{ seat.section_name }}
									</span>
								</div>
							</div>
							<div class="flex justify-between">
								<span class="text-gray-600">Tổng tiền:</span>
								<span
									class="font-bold text-lg text-primary-600"
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
								class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition duration-300"
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
