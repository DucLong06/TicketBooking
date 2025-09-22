# API Documentation

This document outlines the REST API endpoints for the theater ticket booking system. The API follows RESTful conventions and returns JSON responses.

## Base Information

- **Base URL**: `http://localhost:8000/api` (development)
- **API Version**: v1
- **Content Type**: `application/json`
- **Authentication**: JWT Bearer tokens

## Authentication

### Overview
The API uses JSON Web Tokens (JWT) for authentication. Tokens are required for most endpoints and should be included in the Authorization header.

```
Authorization: Bearer <your-jwt-token>
```

### Token Lifecycle
- **Access Token**: 60 minutes lifetime
- **Refresh Token**: 7 days lifetime
- **Auto-refresh**: Implement token refresh in your client

### Authentication Endpoints

#### POST /api/auth/register/
Register a new user account.

**Request:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:** `201 Created`
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_joined": "2024-01-01T10:00:00Z"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

#### POST /api/auth/login/
Authenticate user and obtain tokens.

**Request:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

#### POST /api/auth/token/refresh/
Refresh access token using refresh token.

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### POST /api/auth/logout/
Logout user (blacklist refresh token).

**Headers:** `Authorization: Bearer <access-token>`

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:** `200 OK`
```json
{
  "message": "Successfully logged out"
}
```

## Venues

Manage theater venues and locations.

### Data Model
```json
{
  "id": 1,
  "name": "Grand Theater",
  "address": "123 Main Street, City, State 12345",
  "description": "Historic theater in downtown",
  "capacity": 500,
  "phone": "+1-555-0123",
  "email": "info@grandtheater.com",
  "website": "https://grandtheater.com",
  "image": "https://example.com/media/venues/grand-theater.jpg",
  "amenities": ["parking", "accessibility", "concessions"],
  "is_active": true,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

#### GET /api/venues/
List all active venues.

**Query Parameters:**
- `search` (string): Search by name or address
- `capacity_min` (integer): Minimum capacity
- `capacity_max` (integer): Maximum capacity
- `amenities` (string): Comma-separated amenities filter
- `ordering` (string): Sort by field (`name`, `capacity`, `-created_at`)
- `page` (integer): Page number for pagination
- `page_size` (integer): Items per page (default: 20, max: 100)

**Response:** `200 OK`
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/venues/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Grand Theater",
      "address": "123 Main Street, City, State 12345",
      "capacity": 500,
      "image": "https://example.com/media/venues/grand-theater.jpg",
      "amenities": ["parking", "accessibility"],
      "events_count": 12
    }
  ]
}
```

#### GET /api/venues/{id}/
Get venue details by ID.

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Grand Theater",
  "address": "123 Main Street, City, State 12345",
  "description": "Historic theater in downtown",
  "capacity": 500,
  "phone": "+1-555-0123",
  "email": "info@grandtheater.com",
  "website": "https://grandtheater.com",
  "image": "https://example.com/media/venues/grand-theater.jpg",
  "amenities": ["parking", "accessibility", "concessions"],
  "seating_chart": "https://example.com/media/venues/seating-chart.jpg",
  "upcoming_events": [
    {
      "id": 1,
      "title": "Romeo and Juliet",
      "start_time": "2024-02-01T19:30:00Z",
      "price_range": {"min": 25.00, "max": 85.00}
    }
  ],
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

#### POST /api/venues/ *(Admin only)*
Create a new venue.

**Headers:** `Authorization: Bearer <admin-access-token>`

**Request:**
```json
{
  "name": "New Theater",
  "address": "456 Oak Avenue, City, State 67890",
  "description": "Modern theater facility",
  "capacity": 300,
  "phone": "+1-555-0456",
  "email": "contact@newtheater.com",
  "website": "https://newtheater.com",
  "amenities": ["parking", "accessibility"]
}
```

**Response:** `201 Created`

## Events

Manage theater events and performances.

### Data Model
```json
{
  "id": 1,
  "title": "Romeo and Juliet",
  "description": "Classic Shakespeare tragedy",
  "venue": {
    "id": 1,
    "name": "Grand Theater",
    "address": "123 Main Street"
  },
  "start_time": "2024-02-01T19:30:00Z",
  "end_time": "2024-02-01T22:00:00Z",
  "duration_minutes": 150,
  "category": "drama",
  "price_tiers": [
    {"name": "Orchestra", "price": 85.00, "seats_available": 100},
    {"name": "Mezzanine", "price": 65.00, "seats_available": 80},
    {"name": "Balcony", "price": 25.00, "seats_available": 120}
  ],
  "poster_image": "https://example.com/media/events/romeo-juliet.jpg",
  "gallery_images": [
    "https://example.com/media/events/romeo-1.jpg",
    "https://example.com/media/events/romeo-2.jpg"
  ],
  "age_rating": "PG",
  "language": "English",
  "subtitles": null,
  "tags": ["shakespeare", "drama", "classic"],
  "booking_opens": "2024-01-01T09:00:00Z",
  "booking_closes": "2024-02-01T19:00:00Z",
  "total_seats": 300,
  "available_seats": 245,
  "is_active": true,
  "is_featured": true,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-15T14:30:00Z"
}
```

#### GET /api/events/
List events with filtering and search.

**Query Parameters:**
- `search` (string): Search by title, description, or tags
- `venue` (integer): Filter by venue ID
- `category` (string): Filter by category
- `date_from` (date): Events from this date (YYYY-MM-DD)
- `date_to` (date): Events up to this date (YYYY-MM-DD)
- `price_min` (decimal): Minimum ticket price
- `price_max` (decimal): Maximum ticket price
- `age_rating` (string): Age rating filter
- `is_featured` (boolean): Featured events only
- `has_availability` (boolean): Events with available seats
- `ordering` (string): Sort by field (`start_time`, `-start_time`, `title`, `price`)

**Response:** `200 OK`
```json
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Romeo and Juliet",
      "venue": {
        "id": 1,
        "name": "Grand Theater"
      },
      "start_time": "2024-02-01T19:30:00Z",
      "price_range": {"min": 25.00, "max": 85.00},
      "poster_image": "https://example.com/media/events/romeo-juliet.jpg",
      "available_seats": 245,
      "total_seats": 300,
      "is_featured": true
    }
  ]
}
```

#### GET /api/events/{id}/
Get event details by ID.

**Response:** `200 OK`
```json
{
  "id": 1,
  "title": "Romeo and Juliet",
  "description": "William Shakespeare's timeless tragedy...",
  "venue": {
    "id": 1,
    "name": "Grand Theater",
    "address": "123 Main Street, City, State 12345",
    "capacity": 500
  },
  "start_time": "2024-02-01T19:30:00Z",
  "end_time": "2024-02-01T22:00:00Z",
  "duration_minutes": 150,
  "category": "drama",
  "price_tiers": [
    {"name": "Orchestra", "price": 85.00, "seats_available": 100},
    {"name": "Mezzanine", "price": 65.00, "seats_available": 80},
    {"name": "Balcony", "price": 25.00, "seats_available": 120}
  ],
  "poster_image": "https://example.com/media/events/romeo-juliet.jpg",
  "gallery_images": [
    "https://example.com/media/events/romeo-1.jpg"
  ],
  "age_rating": "PG",
  "language": "English",
  "tags": ["shakespeare", "drama", "classic"],
  "booking_opens": "2024-01-01T09:00:00Z",
  "booking_closes": "2024-02-01T19:00:00Z",
  "cast_and_crew": [
    {"role": "Director", "name": "Jane Smith"},
    {"role": "Romeo", "name": "John Actor"},
    {"role": "Juliet", "name": "Jane Actress"}
  ],
  "reviews_summary": {
    "average_rating": 4.5,
    "total_reviews": 23
  }
}
```

#### GET /api/events/{id}/seats/
Get seat availability for an event.

**Response:** `200 OK`
```json
{
  "event_id": 1,
  "seating_chart": "https://example.com/media/venues/seating-chart.jpg",
  "sections": [
    {
      "name": "Orchestra",
      "price": 85.00,
      "rows": [
        {
          "row": "A",
          "seats": [
            {"number": 1, "status": "available"},
            {"number": 2, "status": "reserved"},
            {"number": 3, "status": "sold"},
            {"number": 4, "status": "available"}
          ]
        }
      ]
    }
  ],
  "legend": {
    "available": "Available for booking",
    "reserved": "Temporarily held",
    "sold": "Already purchased",
    "blocked": "Not available for sale"
  }
}
```

## Bookings

Handle ticket bookings and reservations.

### Data Model
```json
{
  "id": "BK-2024-000123",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  },
  "event": {
    "id": 1,
    "title": "Romeo and Juliet",
    "start_time": "2024-02-01T19:30:00Z",
    "venue": {
      "name": "Grand Theater",
      "address": "123 Main Street"
    }
  },
  "seats": [
    {
      "section": "Orchestra",
      "row": "A",
      "number": 5,
      "price": 85.00
    },
    {
      "section": "Orchestra", 
      "row": "A",
      "number": 6,
      "price": 85.00
    }
  ],
  "booking_date": "2024-01-15T14:30:00Z",
  "status": "confirmed",
  "payment_status": "paid",
  "total_amount": 170.00,
  "fees": {
    "service_fee": 8.50,
    "processing_fee": 3.40
  },
  "grand_total": 181.90,
  "expires_at": "2024-01-15T14:45:00Z",
  "confirmation_code": "ABC123DEF",
  "special_requests": "Wheelchair accessible seating",
  "created_at": "2024-01-15T14:30:00Z",
  "updated_at": "2024-01-15T14:32:00Z"
}
```

#### POST /api/bookings/
Create a new booking (seat reservation).

**Headers:** `Authorization: Bearer <access-token>`

**Request:**
```json
{
  "event_id": 1,
  "seats": [
    {"section": "Orchestra", "row": "A", "number": 5},
    {"section": "Orchestra", "row": "A", "number": 6}
  ],
  "special_requests": "Wheelchair accessible seating"
}
```

**Response:** `201 Created`
```json
{
  "id": "BK-2024-000123",
  "status": "pending",
  "seats": [
    {
      "section": "Orchestra",
      "row": "A", 
      "number": 5,
      "price": 85.00
    },
    {
      "section": "Orchestra",
      "row": "A",
      "number": 6, 
      "price": 85.00
    }
  ],
  "total_amount": 170.00,
  "fees": {
    "service_fee": 8.50,
    "processing_fee": 3.40
  },
  "grand_total": 181.90,
  "expires_at": "2024-01-15T14:45:00Z",
  "payment_url": "https://example.com/payment/BK-2024-000123"
}
```

#### GET /api/bookings/
List user's bookings.

**Headers:** `Authorization: Bearer <access-token>`

**Query Parameters:**
- `status` (string): Filter by status (`pending`, `confirmed`, `cancelled`, `expired`)
- `event` (integer): Filter by event ID
- `date_from` (date): Bookings from this date
- `date_to` (date): Bookings up to this date
- `ordering` (string): Sort by field (`-created_at`, `booking_date`, `status`)

**Response:** `200 OK`
```json
{
  "count": 5,
  "results": [
    {
      "id": "BK-2024-000123",
      "event": {
        "id": 1,
        "title": "Romeo and Juliet",
        "start_time": "2024-02-01T19:30:00Z",
        "poster_image": "https://example.com/media/events/romeo-juliet.jpg"
      },
      "seats_count": 2,
      "status": "confirmed",
      "grand_total": 181.90,
      "booking_date": "2024-01-15T14:30:00Z"
    }
  ]
}
```

#### GET /api/bookings/{id}/
Get booking details by ID.

**Headers:** `Authorization: Bearer <access-token>`

**Response:** `200 OK` - Returns full booking model

#### PATCH /api/bookings/{id}/
Update booking (limited fields).

**Headers:** `Authorization: Bearer <access-token>`

**Request:**
```json
{
  "special_requests": "Updated request"
}
```

#### DELETE /api/bookings/{id}/
Cancel a booking.

**Headers:** `Authorization: Bearer <access-token>`

**Response:** `200 OK`
```json
{
  "message": "Booking cancelled successfully",
  "refund_amount": 181.90,
  "refund_reference": "REF-2024-000456"
}
```

## Payments

Handle payment processing and transactions.

### Data Model
```json
{
  "id": "PAY-2024-000123",
  "booking_id": "BK-2024-000123",
  "amount": 181.90,
  "currency": "VND",
  "payment_method": "vnpay",
  "status": "completed",
  "gateway_transaction_id": "vnpay_20240115_123456",
  "gateway_response": {
    "vnp_TxnRef": "BK-2024-000123",
    "vnp_Amount": "18190000",
    "vnp_ResponseCode": "00",
    "vnp_TransactionStatus": "00"
  },
  "paid_at": "2024-01-15T14:32:00Z",
  "expires_at": "2024-01-15T15:00:00Z",
  "created_at": "2024-01-15T14:30:00Z",
  "updated_at": "2024-01-15T14:32:00Z"
}
```

#### POST /api/payments/
Initiate payment for a booking.

**Headers:** `Authorization: Bearer <access-token>`

**Request:**
```json
{
  "booking_id": "BK-2024-000123",
  "payment_method": "vnpay",
  "return_url": "http://localhost:3000/payment/return"
}
```

**Response:** `201 Created`
```json
{
  "id": "PAY-2024-000123",
  "status": "pending",
  "payment_url": "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html?...",
  "expires_at": "2024-01-15T15:00:00Z"
}
```

#### GET /api/payments/{id}/
Get payment details by ID.

**Headers:** `Authorization: Bearer <access-token>`

**Response:** `200 OK` - Returns full payment model

#### POST /api/payments/{id}/verify/
Verify payment status (webhook endpoint).

**Request:**
```json
{
  "vnp_TxnRef": "BK-2024-000123",
  "vnp_Amount": "18190000",
  "vnp_ResponseCode": "00",
  "vnp_TransactionStatus": "00",
  "vnp_SecureHash": "..."
}
```

**Response:** `200 OK`
```json
{
  "status": "completed",
  "booking_status": "confirmed"
}
```

## User Management

User profile and account management.

#### GET /api/auth/profile/
Get current user profile.

**Headers:** `Authorization: Bearer <access-token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1-555-0123",
  "date_of_birth": "1990-01-01",
  "preferences": {
    "newsletter": true,
    "sms_notifications": false,
    "favorite_genres": ["drama", "comedy"]
  },
  "booking_history_count": 15,
  "total_spent": 2450.00,
  "membership_level": "gold",
  "date_joined": "2023-06-15T10:00:00Z"
}
```

#### PATCH /api/auth/profile/
Update user profile.

**Headers:** `Authorization: Bearer <access-token>`

**Request:**
```json
{
  "first_name": "John",
  "last_name": "Smith", 
  "phone": "+1-555-0124",
  "preferences": {
    "newsletter": false,
    "sms_notifications": true
  }
}
```

## WebSocket Events

Real-time updates via WebSocket connections.

### Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/events/1/seats/');
```

### Event Types

#### Seat Status Updates
```json
{
  "type": "seat_status_update",
  "data": {
    "event_id": 1,
    "seats": [
      {
        "section": "Orchestra",
        "row": "A",
        "number": 5,
        "status": "reserved",
        "reserved_until": "2024-01-15T14:45:00Z"
      }
    ]
  }
}
```

#### Booking Updates  
```json
{
  "type": "booking_update",
  "data": {
    "booking_id": "BK-2024-000123",
    "status": "confirmed",
    "payment_status": "paid"
  }
}
```

## Error Handling

### Standard Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": ["This field is required."],
      "password": ["Password must be at least 8 characters."]
    },
    "timestamp": "2024-01-15T14:30:00Z",
    "request_id": "req_123456"
  }
}
```

### HTTP Status Codes

#### Success Codes
- `200 OK` - Request successful
- `201 Created` - Resource created
- `204 No Content` - Successful deletion

#### Client Error Codes
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict (e.g., seat already booked)
- `422 Unprocessable Entity` - Validation errors

#### Server Error Codes
- `500 Internal Server Error` - Server error
- `502 Bad Gateway` - External service error
- `503 Service Unavailable` - Service temporarily down

### Common Error Codes

#### Authentication Errors
- `AUTH_TOKEN_EXPIRED` - JWT token has expired
- `AUTH_TOKEN_INVALID` - JWT token is invalid
- `AUTH_CREDENTIALS_INVALID` - Username/password incorrect

#### Booking Errors
- `SEAT_NOT_AVAILABLE` - Selected seat is no longer available
- `BOOKING_EXPIRED` - Booking reservation has expired
- `INSUFFICIENT_INVENTORY` - Not enough seats available
- `EVENT_NOT_BOOKABLE` - Event is not open for booking

#### Payment Errors
- `PAYMENT_FAILED` - Payment processing failed
- `PAYMENT_DECLINED` - Payment was declined
- `PAYMENT_TIMEOUT` - Payment session expired

## Rate Limiting

API endpoints are rate-limited to prevent abuse:

- **Authentication endpoints**: 5 requests per minute
- **General API endpoints**: 100 requests per minute  
- **Search endpoints**: 50 requests per minute
- **Booking endpoints**: 10 requests per minute

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642682400
```

## Pagination

List endpoints use cursor-based pagination:

```json
{
  "count": 250,
  "next": "http://localhost:8000/api/events/?cursor=eyJ0aW1lc3RhbXAiOi...",
  "previous": null,
  "results": [...]
}
```

Query parameters:
- `cursor` - Pagination cursor
- `page_size` - Items per page (default: 20, max: 100)

## API Versioning

The API supports versioning through URL prefixes:
- Current version: `/api/v1/`
- Legacy support: `/api/` (defaults to v1)

Version headers:
```
API-Version: 1.0
Accept: application/vnd.theaterapi.v1+json
```

## OpenAPI Specification

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI JSON**: http://localhost:8000/api/schema/

## SDKs and Examples

### JavaScript/TypeScript
```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auto-refresh tokens
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      // Handle token refresh
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await api.post('/auth/token/refresh/', {
            refresh: refreshToken
          });
          localStorage.setItem('access_token', response.data.access);
          return api.request(error.config);
        } catch (refreshError) {
          // Redirect to login
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);
```

### Python
```python
import requests
from typing import Optional

class TheaterAPI:
    def __init__(self, base_url: str, token: Optional[str] = None):
        self.base_url = base_url
        self.session = requests.Session()
        if token:
            self.session.headers.update({
                'Authorization': f'Bearer {token}'
            })
    
    def get_events(self, **params):
        response = self.session.get(f'{self.base_url}/events/', params=params)
        response.raise_for_status()
        return response.json()
    
    def create_booking(self, event_id: int, seats: list):
        data = {'event_id': event_id, 'seats': seats}
        response = self.session.post(f'{self.base_url}/bookings/', json=data)
        response.raise_for_status()
        return response.json()

# Usage
api = TheaterAPI('http://localhost:8000/api', token='your-jwt-token')
events = api.get_events(is_featured=True)
```

This API documentation provides a comprehensive guide for integrating with the theater booking system. For additional support or questions, please refer to the development team.