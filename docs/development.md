# Development Workflow

This guide covers the development workflow, coding standards, and best practices for the theater ticket booking system.

## Development Environment Setup

### Initial Setup
1. Clone the repository and run the setup script
2. Verify all services are running with health checks
3. Create a Django superuser for admin access
4. Load sample data (if available)

### Daily Development Workflow

```bash
# 1. Start your development session
docker-compose up -d db redis backend

# 2. For frontend development
docker-compose up frontend

# 3. View logs during development
docker-compose logs -f backend frontend

# 4. Run tests before committing
docker-compose exec backend python manage.py test
docker-compose run --rm frontend npm run test

# 5. Stop services when done
docker-compose down
```

## Development Guidelines

### Git Workflow
- Use feature branches: `feature/add-seat-selection`
- Write descriptive commit messages
- Squash commits before merging
- Always create pull requests for code review

### Code Organization

#### Backend Structure
```
backend/apps/
├── venues/
│   ├── models.py          # Database models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── urls.py            # URL routing
│   ├── services.py        # Business logic
│   ├── permissions.py     # Access control
│   └── tests/             # Test files
│       ├── test_models.py
│       ├── test_views.py
│       └── test_services.py
```

#### Frontend Structure
```
frontend/src/
├── components/
│   ├── common/            # Reusable UI components
│   ├── layout/            # Layout components
│   └── [feature]/         # Feature-specific components
├── views/                 # Page components
├── stores/                # Pinia state management
├── services/              # API clients
├── composables/           # Vue composables
└── types/                 # TypeScript definitions
```

## Coding Standards

### Backend (Python/Django)

#### Code Style
- Follow PEP 8 style guide
- Use Black for code formatting
- Use isort for import sorting
- Maximum line length: 88 characters

#### Django Best Practices
```python
# models.py - Use descriptive model names
class Event(models.Model):
    title = models.CharField(max_length=200)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    
    class Meta:
        db_table = 'events'
        ordering = ['-start_time']

# serializers.py - Explicit field definitions
class EventSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source='venue.name', read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'venue', 'venue_name', 'start_time']

# views.py - Use ViewSets for CRUD operations
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related('venue')
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

# services.py - Business logic separation
class BookingService:
    @staticmethod
    def create_booking(user, event, seats):
        with transaction.atomic():
            booking = Booking.objects.create(user=user, event=event)
            for seat in seats:
                BookingSeat.objects.create(booking=booking, seat=seat)
            return booking
```

#### Testing Standards
```python
# tests/test_models.py
class EventModelTest(TestCase):
    def setUp(self):
        self.venue = Venue.objects.create(name="Test Venue")
    
    def test_event_creation(self):
        event = Event.objects.create(
            title="Test Event",
            venue=self.venue,
            start_time=timezone.now()
        )
        self.assertEqual(event.title, "Test Event")
        self.assertEqual(str(event), "Test Event")

# tests/test_views.py
class EventViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_list_events(self):
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, 200)
```

### Frontend (Vue 3/TypeScript)

#### Code Style
- Use Prettier for formatting
- Use ESLint with Vue/TypeScript rules
- Use Composition API over Options API
- Use `<script setup>` syntax

#### Vue Best Practices
```vue
<!-- EventCard.vue -->
<template>
  <div class="event-card">
    <h3>{{ event.title }}</h3>
    <p>{{ formatDate(event.startTime) }}</p>
    <BaseButton @click="selectEvent" :disabled="isLoading">
      Select Seats
    </BaseButton>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/common/BaseButton.vue'
import type { Event } from '@/types'

interface Props {
  event: Event
  isLoading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isLoading: false
})

const router = useRouter()

const formatDate = (date: string | Date) => {
  return new Date(date).toLocaleDateString()
}

const selectEvent = () => {
  router.push(`/events/${props.event.id}/seats`)
}
</script>
```

#### State Management (Pinia)
```typescript
// stores/events.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { eventsApi } from '@/services/api/events'
import type { Event } from '@/types'

export const useEventsStore = defineStore('events', () => {
  const events = ref<Event[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const upcomingEvents = computed(() => 
    events.value.filter(event => new Date(event.startTime) > new Date())
  )

  const fetchEvents = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await eventsApi.getEvents()
      events.value = response.data
    } catch (err) {
      error.value = 'Failed to fetch events'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  return {
    events,
    loading,
    error,
    upcomingEvents,
    fetchEvents
  }
})
```

#### Testing Standards
```typescript
// tests/components/EventCard.test.ts
import { mount } from '@vue/test-utils'
import EventCard from '@/components/EventCard.vue'
import type { Event } from '@/types'

describe('EventCard', () => {
  const mockEvent: Event = {
    id: 1,
    title: 'Test Event',
    startTime: '2024-01-01T20:00:00Z',
    venue: { id: 1, name: 'Test Venue' }
  }

  it('renders event information correctly', () => {
    const wrapper = mount(EventCard, {
      props: { event: mockEvent }
    })
    
    expect(wrapper.text()).toContain('Test Event')
    expect(wrapper.find('h3').text()).toBe('Test Event')
  })

  it('emits select event when button clicked', async () => {
    const wrapper = mount(EventCard, {
      props: { event: mockEvent }
    })
    
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted().select).toBeTruthy()
  })
})
```

## Development Tools

### Backend Development

#### Django Management Commands
```bash
# Database operations
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py dbshell

# User management
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py changepassword username

# Development utilities
docker-compose exec backend python manage.py shell
docker-compose exec backend python manage.py collectstatic
docker-compose exec backend python manage.py check --deploy
```

#### Debugging
```python
# Use Django Debug Toolbar (development only)
# Add to urls.py in development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Logging configuration
import logging
logger = logging.getLogger(__name__)
logger.info("Debug information")
logger.error("Error occurred", exc_info=True)
```

### Frontend Development

#### Package Management
```bash
# Install dependencies
docker-compose run --rm frontend npm install

# Add new package
docker-compose run --rm frontend npm install package-name

# Update packages
docker-compose run --rm frontend npm update

# Audit security
docker-compose run --rm frontend npm audit
```

#### Build Tools
```bash
# Development server with hot reload
docker-compose up frontend

# Production build
docker-compose run --rm frontend npm run build

# Preview production build
docker-compose run --rm frontend npm run preview

# Lint and format
docker-compose run --rm frontend npm run lint
docker-compose run --rm frontend npm run format
```

## Database Development

### Migrations
```bash
# Create migration after model changes
docker-compose exec backend python manage.py makemigrations

# Apply migrations
docker-compose exec backend python manage.py migrate

# Show migration status
docker-compose exec backend python manage.py showmigrations

# Create empty migration for data changes
docker-compose exec backend python manage.py makemigrations --empty app_name
```

### Database Schema Best Practices
- Use descriptive table and column names
- Add proper indexes for frequently queried fields
- Use constraints to ensure data integrity
- Plan for data migration in production

## Performance Optimization

### Backend Optimization
```python
# Database query optimization
events = Event.objects.select_related('venue').prefetch_related('bookings')

# Caching frequently accessed data
from django.core.cache import cache

def get_popular_events():
    cache_key = 'popular_events'
    events = cache.get(cache_key)
    if events is None:
        events = Event.objects.filter(is_popular=True)[:10]
        cache.set(cache_key, events, 300)  # 5 minutes
    return events

# Async views for I/O operations
import asyncio
from django.http import JsonResponse

async def async_view(request):
    data = await some_async_operation()
    return JsonResponse(data)
```

### Frontend Optimization
```typescript
// Lazy loading components
const EventDetails = defineAsyncComponent(() =>
  import('@/components/EventDetails.vue')
)

// Debounced search
import { debounce } from 'lodash-es'

const searchEvents = debounce(async (query: string) => {
  if (query.length > 2) {
    await eventsStore.searchEvents(query)
  }
}, 300)

// Virtual scrolling for large lists
import { RecycleScroller } from 'vue-virtual-scroller'
```

## Security Considerations

### Backend Security
- Always validate input data
- Use Django's built-in CSRF protection
- Implement proper authentication and authorization
- Sanitize user-generated content
- Use HTTPS in production
- Keep dependencies updated

### Frontend Security
- Validate user input on the client side
- Sanitize data before displaying
- Use environment variables for API endpoints
- Implement proper error handling
- Keep dependencies updated

## Troubleshooting

### Common Issues

#### Backend Issues
```bash
# Database connection issues
docker-compose logs db
docker-compose exec db psql -U theater_user -d theater_booking

# Migration conflicts
docker-compose exec backend python manage.py migrate --fake-initial

# Permission denied errors
docker-compose exec backend python manage.py collectstatic --clear
```

#### Frontend Issues
```bash
# Node modules issues
docker-compose run --rm frontend rm -rf node_modules
docker-compose run --rm frontend npm install

# Build issues
docker-compose run --rm frontend npm run build -- --debug

# TypeScript errors
docker-compose run --rm frontend npx tsc --noEmit
```

#### Docker Issues
```bash
# Container won't start
docker-compose ps
docker-compose logs [service-name]

# Port conflicts
docker-compose down
lsof -i :3000  # Check what's using the port

# Volume issues
docker-compose down -v  # Remove volumes
docker system prune     # Clean up unused resources
```

## Performance Monitoring

### Backend Monitoring
- Use Django Debug Toolbar in development
- Monitor database query performance
- Track API response times
- Monitor Celery task execution

### Frontend Monitoring
- Use Vue DevTools for component debugging
- Monitor bundle size with webpack-bundle-analyzer
- Track page load times
- Monitor API call performance

## Code Review Checklist

### Backend Checklist
- [ ] Code follows PEP 8 standards
- [ ] Models have proper validation
- [ ] API endpoints have appropriate permissions
- [ ] Database queries are optimized
- [ ] Tests cover new functionality
- [ ] Error handling is implemented
- [ ] Logging is appropriate

### Frontend Checklist
- [ ] Components are properly typed
- [ ] Props and emits are defined
- [ ] Accessibility attributes are included
- [ ] Performance optimizations are applied
- [ ] Tests cover component behavior
- [ ] Error states are handled
- [ ] Loading states are implemented

## Deployment Preparation

### Pre-deployment Checklist
- [ ] All tests pass
- [ ] Database migrations are ready
- [ ] Environment variables are configured
- [ ] Static files are collected
- [ ] Security checks pass
- [ ] Performance benchmarks meet requirements
- [ ] Documentation is updated

### Monitoring Setup
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring (APM)
- [ ] Log aggregation (ELK stack)
- [ ] Health check endpoints
- [ ] Database monitoring
- [ ] Server resource monitoring