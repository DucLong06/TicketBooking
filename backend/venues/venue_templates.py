"""
Venue layout templates for various types of venues. 
"""

HO_GUOM_OPERA_TEMPLATE = {
    "name": "Hồ Gươm Opera - Realistic Layout",
    "type": "Opera",
    "description": "Opera test",
    "floors": [
        {
            "id": "khan_phong_1",
            "name": "KHÁN PHÒNG 1",
            "sections": [
                {
                    "id": "main_floor_1",
                    "name": "Tầng 1 chính",
                    "rows": [
                        # VIP front rows (red/orange in image)
                        {"label": "A", "seats": 20, "numbering": "center_out", "category": "vip",
                         "position_y": 150, "gaps": []},
                        {"label": "B", "seats": 22, "numbering": "center_out", "category": "vip",
                         "position_y": 175, "gaps": []},
                        {"label": "C", "seats": 24, "numbering": "center_out", "category": "vip",
                         "position_y": 200, "gaps": []},
                        {"label": "D", "seats": 26, "numbering": "center_out", "category": "vip",
                         "position_y": 225, "gaps": []},
                        {"label": "E", "seats": 28, "numbering": "center_out", "category": "vip",
                         "position_y": 250, "gaps": []},
                        {"label": "F", "seats": 30, "numbering": "center_out", "category": "vip",
                         "position_y": 275, "gaps": []},
                        {"label": "G", "seats": 32, "numbering": "center_out", "category": "vip",
                         "position_y": 300, "gaps": []},

                        # Standard rows with complex gaps (yellow/gold in image)
                        {"label": "H", "seats": 36, "numbering": "center_out", "category": "standard",
                         "position_y": 325, "gaps": [6, 7, 30, 31]},  # Side aisles
                        {"label": "I", "seats": 38, "numbering": "center_out", "category": "standard",
                         "position_y": 350, "gaps": [6, 7, 32, 33]},
                        {"label": "K", "seats": 40, "numbering": "center_out", "category": "standard",
                         "position_y": 375, "gaps": [6, 7, 34, 35]},
                        {"label": "L", "seats": 42, "numbering": "center_out", "category": "standard",
                         "position_y": 400, "gaps": [6, 7, 36, 37]},
                        {"label": "M", "seats": 44, "numbering": "center_out", "category": "standard",
                         "position_y": 425, "gaps": [5, 6, 7, 37, 38, 39]},  # Wider aisles
                        {"label": "N", "seats": 46, "numbering": "center_out", "category": "standard",
                         "position_y": 450, "gaps": [5, 6, 7, 39, 40, 41]},
                        {"label": "O", "seats": 48, "numbering": "center_out", "category": "standard",
                         "position_y": 475, "gaps": [4, 5, 6, 7, 41, 42, 43, 44]},  # Even wider

                        # Economy back rows (pink/purple in image)
                        {"label": "P", "seats": 50, "numbering": "center_out", "category": "economy",
                         "position_y": 500, "gaps": [4, 5, 6, 7, 43, 44, 45, 46]},
                        {"label": "Q", "seats": 48, "numbering": "center_out", "category": "economy",
                         "position_y": 525, "gaps": [4, 5, 6, 41, 42, 43]},
                        {"label": "R", "seats": 46, "numbering": "center_out", "category": "economy",
                         "position_y": 550, "gaps": [4, 5, 39, 40, 41]},
                        {"label": "S", "seats": 44, "numbering": "center_out", "category": "economy",
                         "position_y": 575, "gaps": [4, 37, 38, 39]},
                        {"label": "T", "seats": 42, "numbering": "center_out", "category": "economy",
                         "position_y": 600, "gaps": [3, 35, 36, 37]},
                        {"label": "U", "seats": 40, "numbering": "center_out", "category": "economy",
                         "position_y": 625, "gaps": [3, 33, 34, 35]},
                    ]
                },
                # LG Left boxes (vertical blue in image)
                {
                    "id": "loge_left",
                    "name": "Loge Trái",
                    "rows": [
                        {"label": "LG", "seats": 8, "numbering": "vertical", "category": "loge",
                         "position_y": 300, "layout": "vertical_left"}
                    ]
                },
                # LG Right boxes
                {
                    "id": "loge_right",
                    "name": "Loge Phải",
                    "rows": [
                        {"label": "LG", "seats": 8, "numbering": "vertical", "category": "loge",
                         "position_y": 300, "layout": "vertical_right"}
                    ]
                }
            ]
        },
        {
            "id": "khan_phong_2",
            "name": "KHÁN PHÒNG 2",
            "sections": [
                {
                    "id": "upper_level",
                    "name": "Tầng trên",
                    "rows": [
                        # Upper level teal/turquoise seats
                        {"label": "AA", "seats": 16, "numbering": "center_out", "category": "upper",
                         "position_y": 720, "gaps": []},
                        {"label": "BB", "seats": 18, "numbering": "center_out", "category": "upper",
                         "position_y": 745, "gaps": []},
                        {"label": "CC", "seats": 20, "numbering": "center_out", "category": "upper",
                         "position_y": 770, "gaps": []},

                        # Main upper floor (blue in image)
                        {"label": "A", "seats": 24, "numbering": "center_out", "category": "balcony",
                         "position_y": 795, "gaps": [4, 5, 19, 20]},
                        {"label": "B", "seats": 26, "numbering": "center_out", "category": "balcony",
                         "position_y": 820, "gaps": [4, 5, 21, 22]},
                        {"label": "C", "seats": 28, "numbering": "center_out", "category": "balcony",
                         "position_y": 845, "gaps": [4, 5, 23, 24]},
                        {"label": "D", "seats": 30, "numbering": "center_out", "category": "balcony",
                         "position_y": 870, "gaps": [4, 5, 25, 26]},
                        {"label": "E", "seats": 32, "numbering": "center_out", "category": "balcony",
                         "position_y": 895, "gaps": [4, 5, 27, 28]},
                        {"label": "F", "seats": 34, "numbering": "center_out", "category": "balcony",
                         "position_y": 920, "gaps": [4, 5, 29, 30]},
                        {"label": "G", "seats": 30, "numbering": "center_out", "category": "balcony",
                         "position_y": 945, "gaps": [3, 4, 26, 27]},
                        {"label": "H", "seats": 20, "numbering": "center_out", "category": "balcony",
                         "position_y": 970, "gaps": [2, 3, 17, 18]},
                        {"label": "I", "seats": 10, "numbering": "center_out", "category": "balcony",
                         "position_y": 995, "gaps": [1, 9]},
                    ]
                }
            ]
        }
    ]
}

STANDARD_THEATER_TEMPLATE = {
    "name": "Standard Theater Layout",
    "type": "theater",
    "description": "Layout rạp hát tiêu chuẩn",
    "dimensions": {
        "width": 600,
        "height": 500
    },
    "floors": [
        {
            "id": "main_floor",
            "name": "Tầng chính",
            "level": 1,
            "sections": [
                {
                    "id": "orchestra",
                    "name": "Orchestra",
                    "rows": [
                        {
                            "label": "A",
                            "seats": 20,
                            "numbering": "left_to_right",
                            "category": "premium"
                        },
                        {
                            "label": "B",
                            "seats": 22,
                            "numbering": "left_to_right",
                            "category": "premium"
                        }
                    ]
                }
            ]
        }
    ],
    "price_categories": {
        "premium": {
            "name": "Premium",
            "base_price": 500000,
            "color": "#E74C3C"
        },
        "standard": {
            "name": "Standard",
            "base_price": 300000,
            "color": "#3498DB"
        }
    }
}

VENUE_TEMPLATES = {
    'ho_guom_opera': HO_GUOM_OPERA_TEMPLATE,
    'standard_theater': STANDARD_THEATER_TEMPLATE,
}


def get_template(template_name):
    return VENUE_TEMPLATES.get(template_name)


def get_templates_by_type(venue_type):
    return {
        name: template for name, template in VENUE_TEMPLATES.items()
        if template['type'] == venue_type
    }


def get_venue_type_choices():
    from .models import VENUE_TYPES
    return VENUE_TYPES
