export const theaterLayout = {
    venue: {
        name: "Hồ Gươm Opera",
        sections: [
            // TẦNG 1
            {
                id: "floor1",
                name: "Tầng 1",
                rows: [
                    // Hàng A - VIP (cam)
                    { id: "A", label: "A", seats: 20, category: "vip", color: "orange" },
                    // Hàng B-F - VIP (cam) 
                    { id: "B", label: "B", seats: 22, category: "vip", color: "orange" },
                    { id: "C", label: "C", seats: 24, category: "vip", color: "orange" },
                    { id: "D", label: "D", seats: 26, category: "vip", color: "orange" },
                    { id: "E", label: "E", seats: 28, category: "vip", color: "orange" },
                    { id: "F", label: "F", seats: 30, category: "vip", color: "orange" },
                    // Hàng G - Standard (cam/vàng)
                    { id: "G", label: "G", seats: 32, category: "standard", color: "orange" },

                    // Hàng H-O - Standard (xanh lá)
                    { id: "H", label: "H", seats: 34, category: "standard", color: "green", aisles: [7, 27] },
                    { id: "I", label: "I", seats: 36, category: "standard", color: "green", aisles: [6, 30] },
                    { id: "K", label: "K", seats: 38, category: "economy", color: "green", aisles: [6, 32] },
                    { id: "L", label: "L", seats: 40, category: "economy", color: "green", aisles: [6, 34] },
                    { id: "M", label: "M", seats: 42, category: "economy", color: "green", aisles: [6, 36] },
                    { id: "N", label: "N", seats: 44, category: "economy", color: "green", aisles: [6, 38] },
                    { id: "O", label: "O", seats: 46, category: "economy", color: "green", aisles: [6, 40] },

                    // Hàng P-Q - Economy (đỏ)
                    { id: "P", label: "P", seats: 48, category: "economy", color: "red", aisles: [6, 24, 42] },
                    { id: "Q", label: "Q", seats: 50, category: "economy", color: "red", aisles: [6, 44] },

                    // Hàng R - Balcony center (xanh dương)
                    { id: "R", label: "R", seats: 30, category: "balcony", color: "blue", aisles: [15] },

                    // Hàng S-U - Upper balcony (tím/hồng)
                    { id: "S", label: "S", seats: 28, category: "upper", color: "purple", aisles: [14] },
                    { id: "T", label: "T", seats: 26, category: "upper", color: "pink", aisles: [8, 18] },
                    { id: "U", label: "U", seats: 24, category: "upper", color: "pink", aisles: [8, 16] }
                ]
            },

            // LOGE boxes (LG)
            {
                id: "loge-left",
                name: "Loge Trái",
                rows: [
                    { id: "LG-L", label: "LG", seats: 4, category: "loge", color: "purple", side: "left" }
                ]
            },
            {
                id: "loge-right",
                name: "Loge Phải",
                rows: [
                    { id: "LG-R", label: "LG", seats: 4, category: "loge", color: "purple", side: "right" }
                ]
            },

            // TẦNG 2
            {
                id: "floor2",
                name: "Tầng 2",
                rows: [
                    // Upper rows
                    { id: "AA", label: "AA", seats: 16, category: "upper", color: "green" },
                    { id: "BB", label: "BB", seats: 18, category: "upper", color: "green" },
                    { id: "CC", label: "CC", seats: 20, category: "upper", color: "green" },

                    // Main floor 2 rows
                    { id: "A2", label: "A", seats: 24, category: "standard", color: "green" },
                    { id: "B2", label: "B", seats: 26, category: "standard", color: "green" },
                    { id: "C2", label: "C", seats: 28, category: "standard", color: "green" },
                    { id: "D2", label: "D", seats: 30, category: "economy", color: "green" },
                    { id: "E2", label: "E", seats: 32, category: "economy", color: "red" },
                    { id: "F2", label: "F", seats: 34, category: "economy", color: "red" },

                    // Side boxes floor 2
                    { id: "G2", label: "G", seats: 6, category: "box", color: "pink", side: "left" },
                    { id: "H2", label: "H", seats: 4, category: "box", color: "pink", side: "right" },
                    { id: "I2", label: "I", seats: 3, category: "box", color: "pink", side: "right" }
                ]
            }
        ]
    },

    // Price categories
    priceCategories: {
        vip: { name: "VIP", price: 2500000, baseColor: "orange" },
        standard: { name: "Standard", price: 1500000, baseColor: "blue" },
        economy: { name: "Economy", price: 1000000, baseColor: "green" },
        balcony: { name: "Balcony", price: 1200000, baseColor: "blue" },
        upper: { name: "Upper", price: 800000, baseColor: "purple" },
        loge: { name: "Loge", price: 3000000, baseColor: "purple" },
        box: { name: "Box", price: 2000000, baseColor: "pink" }
    }
}

// Generate seats for the theater
export function generateTheaterSeats() {
    const seats = []
    let seatId = 1

    theaterLayout.venue.sections.forEach(section => {
        section.rows.forEach(row => {
            for (let i = 1; i <= row.seats; i++) {
                // Random status for demo
                const randomStatus = Math.random()
                let status = 'available'
                if (randomStatus > 0.85) status = 'sold'
                else if (randomStatus > 0.80) status = 'reserved'

                seats.push({
                    id: `${row.id}-${i}`,
                    uniqueId: seatId++,
                    row: row.label,
                    number: i,
                    sectionId: section.id,
                    sectionName: section.name,
                    category: row.category,
                    price: theaterLayout.priceCategories[row.category].price,
                    color: row.color,
                    side: row.side || 'center',
                    status: status,
                    hasAisleLeft: row.aisles && row.aisles.includes(i - 1),
                    hasAisleRight: row.aisles && row.aisles.includes(i)
                })
            }
        })
    })

    return seats
}