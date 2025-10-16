import api from './index'

export const posterAPI = {
    // Get all active posters
    getPosters() {
        return api.get('/posters/')
    }
}