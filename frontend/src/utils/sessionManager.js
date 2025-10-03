const SESSION_SCHEMA = {
    session_id: { required: true, type: 'string' },
    selectedPerformance: { required: false, type: 'object' },
    selectedSeats: { required: false, type: 'array' },
    reservationExpiry: { required: false, type: 'string' },
    bookingData: { required: false, type: 'object' },
}

export const sessionManager = {
    validateSession(requiredKeys = []) {
        for (const key of requiredKeys) {
            const schema = SESSION_SCHEMA[key]
            if (!schema) continue

            const value = sessionStorage.getItem(key)
            if (schema.required && !value) {
                return false
            }

            // Validate type
            if (value) {
                try {
                    const parsed = JSON.parse(value)
                    if (schema.type === 'array' && !Array.isArray(parsed)) {
                        return false
                    }
                    if (schema.type === 'object' && typeof parsed !== 'object') {
                        return false
                    }
                } catch (e) {
                    if (schema.type !== 'string') {
                        return false
                    }
                }
            }
        }
        return true
    },

    clearBookingSession() {
        const keysToKeep = ['zoom_instructions_seen']
        const allKeys = Object.keys(localStorage)

        allKeys.forEach(key => {
            if (!keysToKeep.includes(key)) {
                sessionStorage.removeItem(key)
            }
        })
    },

    // Get typed value
    get(key) {
        const value = sessionStorage.getItem(key)
        if (!value) return null

        try {
            return JSON.parse(value)
        } catch {
            return value
        }
    },

    // Set typed value
    set(key, value) {
        const stringValue = typeof value === 'string'
            ? value
            : JSON.stringify(value)
        sessionStorage.setItem(key, stringValue)
    }
}