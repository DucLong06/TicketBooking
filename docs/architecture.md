# Architecture Overview

This document provides a comprehensive overview of the theater ticket booking system architecture, design decisions, and technical implementation details.

## System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │   Mobile App    │    │   Admin Panel   │
│   (Vue 3 SPA)   │    │   (Future)      │    │   (Django)      │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
              ┌─────────────────────────────────────┐
              │            Nginx                    │
              │      (Reverse Proxy & SSL)          │
              └─────────────────┬───────────────────┘
                                │
              ┌─────────────────────────────────────┐
              │         Load Balancer               │
              │       (Future Scaling)              │
              └─────────────────┬───────────────────┘
                                │
          ┌─────────────────────────────────────────────────┐
          │                Django Backend                   │
          │  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
          │  │   REST API  │  │  WebSocket  │  │  Admin  │ │
          │  │    (DRF)    │  │ (Channels)  │  │   UI    │ │
          │  └─────────────┘  └─────────────┘  └─────────┘ │
          └─────────────────┬───────────────────────────────┘
                            │
          ┌─────────────────────────────────────────────────┐
          │              Background Services                │
          │  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
          │  │   Celery    │  │   Celery    │  │  Redis  │ │
          │  │   Worker    │  │    Beat     │  │ Message │ │
          │  └─────────────┘  └─────────────┘  └─────────┘ │
          └─────────────────┬───────────────────────────────┘
                            │
          ┌─────────────────────────────────────────────────┐
          │               Data Layer                        │
          │  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
          │  │ PostgreSQL  │  │    Redis    │  │  Media  │ │
          │  │ (Primary)   │  │   (Cache)   │  │ Storage │ │
          │  └─────────────┘  └─────────────┘  └─────────┘ │
          └─────────────────────────────────────────────────┘
```

### Component Interaction Flow

```
Frontend (Vue 3) → API Request → Nginx → Django → Database
                                    ↓
WebSocket Connection → Django Channels → Redis → Real-time Updates
                                    ↓
Background Tasks → Celery Workers → Redis Queue → Email/Reports
```

## Technology Stack

### Frontend Layer
- **Vue 3**: Progressive JavaScript framework with Composition API
- **Pinia**: Lightweight state management for Vue
- **Vue Router**: Official routing library for SPA navigation
- **TailwindCSS**: Utility-first CSS framework for responsive design
- **TypeScript**: Type safety and better development experience
- **Vite**: Fast build tool and development server
- **VueUse**: Collection of essential Vue composition utilities

### Backend Layer
- **Django 5.0**: High-level Python web framework
- **Django REST Framework**: Powerful toolkit for building REST APIs
- **Django Channels**: WebSocket and async support
- **Celery**: Distributed task queue for background processing
- **JWT Authentication**: Secure token-based authentication
- **Django CORS Headers**: Cross-origin resource sharing support

### Data Layer
- **PostgreSQL 15**: Primary relational database
- **Redis 7**: In-memory cache and message broker
- **Django ORM**: Object-relational mapping for database operations
- **Connection Pooling**: Efficient database connection management

### Infrastructure Layer
- **Docker**: Containerization for consistent environments
- **Docker Compose**: Multi-container application orchestration
- **Nginx**: Web server and reverse proxy
- **Gunicorn**: WSGI HTTP Server for Python applications (production)
- **SSL/TLS**: Secure communication encryption

## Core Applications

### Venues App
**Purpose**: Manage theater venues and locations

**Models:**
- `Venue`: Theater locations with capacity and amenities
- `Section`: Seating sections within venues (Orchestra, Balcony, etc.)
- `Seat`: Individual seats with pricing tiers

**Key Features:**
- Venue management with detailed information
- Flexible seating chart configuration
- Amenity tracking (parking, accessibility, etc.)
- Capacity and layout management

### Events App
**Purpose**: Manage performances and shows

**Models:**
- `Event`: Theater performances with scheduling
- `EventSeat`: Seat availability and pricing per event
- `EventImage`: Gallery images for events
- `Review`: User reviews and ratings

**Key Features:**
- Event scheduling and management
- Dynamic pricing per seating section
- Image gallery and media management
- Review and rating system
- Category and tag organization

### Bookings App
**Purpose**: Handle ticket reservations and purchases

**Models:**
- `Booking`: Customer reservations with status tracking
- `BookingSeat`: Individual seat selections
- `BookingHistory`: Audit trail of booking changes
- `Reservation`: Temporary seat holds during checkout

**Key Features:**
- Seat selection and reservation system
- Booking lifecycle management (pending → confirmed → completed)
- Automatic expiration of unpaid reservations
- Booking modification and cancellation
- Group booking support

### Payments App
**Purpose**: Process payments and financial transactions

**Models:**
- `Payment`: Transaction records with gateway integration
- `PaymentMethod`: Supported payment options
- `Refund`: Refund processing and tracking
- `Invoice`: Receipt and invoice generation

**Key Features:**
- VNPAY payment gateway integration
- Secure payment processing
- Automated refund handling
- Invoice generation and email delivery
- Payment status webhooks

## Database Design

### Entity Relationship Diagram

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    User     │    │   Venue     │    │   Event     │
│             │    │             │    │             │
│ id (PK)     │    │ id (PK)     │    │ id (PK)     │
│ username    │    │ name        │    │ title       │
│ email       │    │ address     │    │ description │
│ password    │    │ capacity    │    │ venue (FK)  │
│ ...         │    │ ...         │    │ start_time  │
└─────────────┘    └─────────────┘    │ end_time    │
        │                   │         │ ...         │
        │                   │         └─────────────┘
        │                   │                │
        │          ┌─────────────┐          │
        │          │   Section   │          │
        │          │             │          │
        │          │ id (PK)     │          │
        │          │ venue (FK)  │          │
        │          │ name        │          │
        │          │ ...         │          │
        │          └─────────────┘          │
        │                   │               │
        │          ┌─────────────┐          │
        │          │    Seat     │          │
        │          │             │          │
        │          │ id (PK)     │          │
        │          │ section(FK) │          │
        │          │ row         │          │
        │          │ number      │          │
        │          └─────────────┘          │
        │                   │               │
        │                   └───────────────┼─────────────┐
        │                                   │             │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│   Booking   │    │ BookingSeat │    │ EventSeat   │    │
│             │    │             │    │             │    │
│ id (PK)     │    │ id (PK)     │    │ id (PK)     │────┘
│ user (FK)   │────│ booking(FK) │    │ event (FK)  │
│ event (FK)  │    │ seat (FK)   │────│ seat (FK)   │
│ status      │    │ price       │    │ price       │
│ total       │    │ ...         │    │ is_sold     │
│ ...         │    └─────────────┘    │ ...         │
└─────────────┘                       └─────────────┘
        │
        │
┌─────────────┐
│   Payment   │
│             │
│ id (PK)     │
│ booking(FK) │
│ amount      │
│ status      │
│ gateway_id  │
│ ...         │
└─────────────┘
```

### Key Design Decisions

#### 1. Normalized Database Structure
- Separation of venues, events, and bookings for flexibility
- Dedicated seat management for dynamic pricing
- Audit trails for critical operations

#### 2. Soft Delete Pattern
```python
class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

#### 3. Optimized Queries
- Select/prefetch related for reducing N+1 queries
- Database indexes on frequently queried fields
- Query optimization for seat availability checks

## API Architecture

### RESTful Design Principles

#### Resource-Based URLs
```
/api/venues/              # Venue collection
/api/venues/{id}/         # Specific venue
/api/venues/{id}/events/  # Venue's events
/api/events/              # Event collection
/api/events/{id}/seats/   # Event seating
/api/bookings/            # User bookings
/api/payments/            # Payment processing
```

#### HTTP Methods
- `GET`: Retrieve resources
- `POST`: Create new resources
- `PUT/PATCH`: Update existing resources
- `DELETE`: Remove resources

#### Response Format
```json
{
  "data": { ... },          // Main response data
  "meta": {                 // Metadata
    "pagination": { ... },
    "timestamp": "...",
    "version": "1.0"
  },
  "errors": [ ... ]         // Error information
}
```

### Authentication & Authorization

#### JWT Token Flow
```
1. User Login → JWT Access + Refresh Tokens
2. API Request → Include Bearer Token
3. Token Validation → Allow/Deny Access
4. Token Refresh → Extend Session
5. Logout → Blacklist Tokens
```

#### Permission Levels
- **Anonymous**: Public venue/event information
- **Authenticated**: Booking creation and management
- **Staff**: Event management and reports
- **Admin**: Full system access

### API Security

#### Input Validation
```python
class BookingSerializer(serializers.ModelSerializer):
    seats = serializers.ListField(
        child=SeatSelectionSerializer(),
        min_length=1,
        max_length=10
    )
    
    def validate_seats(self, value):
        # Custom validation logic
        return value
```

#### Rate Limiting
```python
# Django settings
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'booking': '10/minute'
    }
}
```

## Real-Time Features

### WebSocket Architecture

#### Django Channels Integration
```python
# WebSocket routing
websocket_urlpatterns = [
    path('ws/events/<int:event_id>/seats/', SeatConsumer.as_asgi()),
    path('ws/bookings/<str:booking_id>/', BookingConsumer.as_asgi()),
]

# Consumer implementation
class SeatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.group_name = f'event_{self.event_id}_seats'
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
```

#### Real-Time Events
1. **Seat Status Updates**: Live seat availability changes
2. **Booking Updates**: Payment confirmations and status changes
3. **Event Updates**: Last-minute event information changes
4. **System Notifications**: Maintenance alerts and announcements

### Caching Strategy

#### Redis Cache Layers
```python
# Django cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Cache usage patterns
@cache_page(60 * 15)  # 15 minutes
def event_list(request):
    return EventViewSet.as_view({'get': 'list'})(request)

# Manual caching
def get_popular_events():
    cache_key = 'popular_events'
    events = cache.get(cache_key)
    if not events:
        events = Event.objects.filter(is_featured=True)[:10]
        cache.set(cache_key, events, 60 * 30)  # 30 minutes
    return events
```

#### Cache Invalidation
- Time-based expiration for static content
- Event-driven invalidation for dynamic data
- Cache warming for frequently accessed data

## Background Processing

### Celery Task Architecture

#### Task Categories
```python
# Email notifications
@shared_task
def send_booking_confirmation_email(booking_id):
    booking = Booking.objects.get(id=booking_id)
    send_mail(
        subject=f'Booking Confirmation - {booking.event.title}',
        message=render_to_string('emails/booking_confirmation.html', {
            'booking': booking
        }),
        recipient_list=[booking.user.email]
    )

# Payment processing
@shared_task
def process_payment_webhook(payment_data):
    # Handle payment gateway webhooks
    payment = Payment.objects.get(gateway_id=payment_data['id'])
    payment.update_status(payment_data['status'])

# Scheduled tasks
@periodic_task(run_every=crontab(minute=0, hour=2))  # Daily at 2 AM
def cleanup_expired_bookings():
    expired_bookings = Booking.objects.filter(
        status='pending',
        expires_at__lt=timezone.now()
    )
    for booking in expired_bookings:
        booking.cancel()
```

#### Task Monitoring
- Celery Flower for task monitoring
- Error tracking and retry mechanisms
- Task result storage and retrieval

## Frontend Architecture

### Vue 3 Application Structure

#### Component Architecture
```
src/
├── components/
│   ├── common/          # Reusable UI components
│   │   ├── BaseButton.vue
│   │   ├── BaseModal.vue
│   │   └── LoadingSpinner.vue
│   ├── layout/          # Layout components
│   │   ├── AppHeader.vue
│   │   ├── AppFooter.vue
│   │   └── Sidebar.vue
│   └── features/        # Feature-specific components
│       ├── EventCard.vue
│       ├── SeatMap.vue
│       └── BookingForm.vue
├── views/               # Page components
├── stores/              # Pinia state stores
├── services/            # API clients
├── composables/         # Vue composables
└── types/               # TypeScript definitions
```

#### State Management (Pinia)
```typescript
// stores/events.ts
export const useEventsStore = defineStore('events', () => {
  const events = ref<Event[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchEvents = async (filters?: EventFilters) => {
    loading.value = true
    try {
      const response = await eventsApi.getEvents(filters)
      events.value = response.data
    } catch (err) {
      error.value = 'Failed to fetch events'
    } finally {
      loading.value = false
    }
  }

  const upcomingEvents = computed(() =>
    events.value.filter(event => 
      new Date(event.startTime) > new Date()
    )
  )

  return {
    events,
    loading,
    error,
    fetchEvents,
    upcomingEvents
  }
})
```

#### API Client Architecture
```typescript
// services/api/client.ts
class ApiClient {
  private axios: AxiosInstance

  constructor(baseURL: string) {
    this.axios = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    this.setupInterceptors()
  }

  private setupInterceptors() {
    // Request interceptor for auth tokens
    this.axios.interceptors.request.use(config => {
      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Response interceptor for token refresh
    this.axios.interceptors.response.use(
      response => response,
      async error => {
        if (error.response?.status === 401) {
          await this.refreshToken()
          return this.axios.request(error.config)
        }
        return Promise.reject(error)
      }
    )
  }
}
```

## Security Architecture

### Authentication Security
- JWT tokens with short expiration times
- Refresh token rotation
- Secure token storage (httpOnly cookies in production)
- Password hashing with Django's PBKDF2

### API Security
- CORS configuration for trusted origins
- Rate limiting to prevent abuse
- Input validation and sanitization
- SQL injection prevention via ORM

### Data Protection
- Sensitive data encryption at rest
- HTTPS enforcement in production
- Personal data anonymization for analytics
- GDPR compliance for user data

### Infrastructure Security
- Container security scanning
- Dependency vulnerability monitoring
- Environment variable isolation
- Database access controls

## Performance Optimization

### Backend Optimization
```python
# Database query optimization
def get_events_with_venue_info():
    return Event.objects.select_related('venue').prefetch_related(
        'eventseat_set__seat__section'
    ).filter(is_active=True)

# API response optimization
class EventSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source='venue.name', read_only=True)
    available_seats = serializers.SerializerMethodField()
    
    def get_available_seats(self, obj):
        # Cached calculation
        cache_key = f'event_{obj.id}_available_seats'
        count = cache.get(cache_key)
        if count is None:
            count = obj.get_available_seat_count()
            cache.set(cache_key, count, 60 * 5)  # 5 minutes
        return count
```

### Frontend Optimization
```typescript
// Lazy loading for routes
const routes = [
  {
    path: '/events/:id',
    component: () => import('@/views/EventDetailsPage.vue')
  }
]

// Component lazy loading
const EventDetails = defineAsyncComponent(() =>
  import('@/components/EventDetails.vue')
)

// API request optimization
const debouncedSearch = debounce((query: string) => {
  if (query.length > 2) {
    eventsStore.searchEvents(query)
  }
}, 300)
```

### Database Optimization
- Database indexing on frequently queried columns
- Connection pooling for efficient resource usage
- Query result caching for expensive operations
- Database-level constraints for data integrity

## Monitoring and Observability

### Application Monitoring
- Health check endpoints for service status
- Performance metrics collection
- Error tracking and alerting
- User activity analytics

### Infrastructure Monitoring
- Container resource usage
- Database performance metrics
- Network latency monitoring
- Disk space and memory usage

### Logging Strategy
```python
# Django logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## Deployment Architecture

### Container Orchestration
```yaml
# docker-compose.yml structure
services:
  nginx:      # Reverse proxy and static file serving
  backend:    # Django application server
  frontend:   # Vue.js development server (dev only)
  celery:     # Background task worker
  db:         # PostgreSQL database
  redis:      # Cache and message broker
```

### Production Considerations
- Multi-stage Docker builds for optimized images
- Environment-specific configuration management
- Automated database migrations
- Blue-green deployment strategy
- Load balancing for high availability

### Scaling Strategy
- Horizontal scaling of Django workers
- Database read replicas for query optimization
- CDN integration for static asset delivery
- Redis clustering for cache scaling

## Future Architecture Considerations

### Microservices Migration
- Service decomposition strategy
- API gateway implementation  
- Service mesh for communication
- Distributed tracing

### Mobile Application
- React Native or Flutter implementation
- Shared API endpoints
- Push notification system
- Offline functionality

### Advanced Features
- Machine learning for event recommendations
- Real-time analytics dashboard
- Multi-language support
- Third-party integrations (social media, calendar apps)

### Scalability Improvements
- Event sourcing for audit trails
- CQRS pattern for read/write separation
- Message queues for service decoupling
- Geographic distribution for global users

This architecture supports the current requirements while providing flexibility for future enhancements and scaling needs.