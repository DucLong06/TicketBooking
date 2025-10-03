// frontend/src/composables/useContact.js
import { ref, onMounted } from 'vue'
import { contactAPI } from '../api/contact'

const contactInfo = ref(null)
const loading = ref(false)
const error = ref(null)

export function useContact() {
    const fetchContactInfo = async () => {
        // Return cached data if available
        if (contactInfo.value) {
            return contactInfo.value
        }

        loading.value = true
        error.value = null

        try {
            const response = await contactAPI.getContactInfo()
            contactInfo.value = response.data
            return contactInfo.value
        } catch (err) {
            error.value = err
            console.error('Error fetching contact info:', err)
            // Return fallback data
            return {
                name: 'Theater Booking',
                hotline: '0962989856',
                hotline_display: '0962.98.98.56',
                support_email: 'duongcamart@gmail.com',
                facebook_url: 'https://www.facebook.com/nhackichgiacmochipheo',
                tiktok_url: 'https://www.tiktok.com/@giacmo.chipheo',
                instagram_url: '',
                website_url: '',
                copyright_text: 'GMCP by duongcamart'
            }
        } finally {
            loading.value = false
        }
    }

    return {
        contactInfo,
        loading,
        error,
        fetchContactInfo
    }
}