import api from './index'

export const contactAPI = {
    // Get contact information
    getContactInfo() {
        return api.get('/contact-info/')
    }
}