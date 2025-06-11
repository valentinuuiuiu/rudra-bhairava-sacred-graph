# Plan de Îmbunătățiri Arhitecturale

## 1. Separarea Concern-urilor Mixte în Views

**Problema curentă:** 
- View-urile conțin logică de afișare, validare și business logic amestecate
- Exemple din `marketplace/views.py` și `piata_ro/views.py`

**Recomandări:**
```python
# Bad - Mixed concerns
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if not listing.is_active and not request.user.is_staff:
        raise Http404
    # Business logic
    similar = Listing.objects.filter(
        category=listing.category
    ).exclude(pk=pk)[:4]
    # Presentation logic
    return render(request, 'listing_detail.html', {
        'listing': listing,
        'similar': similar
    })

# Good - Separated concerns
class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listing_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['similar'] = self.get_similar_listings()
        return context
    
    def get_similar_listings(self):
        return Listing.objects.filter(
            category=self.object.category
        ).exclude(pk=self.object.pk)[:4]
```

**Beneficii:**
- Cod mai testabil și mai ușor de întreținut
- Respectă principiul Single Responsibility
- Facilitatează reutilizarea componentelor

## 2. Implementarea Stratului de Cache

**Problema curentă:**
- Lipsa mecanismelor de caching pentru resursele statice și dinamice
- Solicitări repetate la baza de date pentru aceleași date

**Recomandări:**
```python
# settings.py - Configurare cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# views.py - Utilizare cache
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache pentru 15 minute
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

# models.py - Cache la nivel de model
from django.core.cache import cache

class Listing(models.Model):
    # ...
    
    @classmethod
    def get_featured_listings(cls):
        cache_key = 'featured_listings'
        listings = cache.get(cache_key)
        if not listings:
            listings = list(cls.objects.filter(is_featured=True)[:8])
            cache.set(cache_key, listings, 60 * 60)  # 1 oră
        return listings
```

**Beneficii:**
- Reducere semnificativă a încărcării bazei de date
- Îmbunătățire a timpilor de răspuns
- Scalabilitate mai bună

## 3. Rezolvarea Dependințelor Circulare

**Problema curentă:**
- Importuri circulare între module (ex: models.py și services.py)
- Cod tightly coupled

**Recomandări:**
```python
# Soluție 1: Utilizare interfete abstracte
# services/listing_service.py
from abc import ABC, abstractmethod

class ListingServiceInterface(ABC):
    @abstractmethod
    def get_featured_listings(self):
        pass

# services/listing_service_impl.py
from .listing_service import ListingServiceInterface

class ListingService(ListingServiceInterface):
    def get_featured_listings(self):
        from marketplace.models import Listing
        return Listing.objects.filter(is_featured=True)[:8]

# Soluție 2: Dependency Injection
class ListingView(View):
    def __init__(self, listing_service: ListingServiceInterface):
        self.listing_service = listing_service
        
    def get(self, request):
        listings = self.listing_service.get_featured_listings()
        return render(...)
```

**Beneficii:**
- Cod mai modular și mai ușor de testat
- Eliminarea dependințelor circulare
- Respectă principiul Dependency Inversion

## 4. Optimizarea Interogărilor la Bază de Date

**Problema curentă:**
- N+1 query problems în multiple view-uri
- Lipsa utilizării select_related/prefetch_related
- Lipsa indexărilor optime

**Recomandări:**
```python
# Bad - N+1 queries
listings = Listing.objects.all()
for listing in listings:
    print(listing.category.name)  # Query separat pentru fiecare categorie

# Good - Optimizat
listings = Listing.objects.select_related('category').all()
for listing in listings:
    print(listing.category.name)  # Doar 1 query

# Adăugare indexuri în models.py
class Listing(models.Model):
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        db_index=True  # Adăugare index
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True  # Index pentru filtrare cronologică
    )

# Utilizare annotate și aggregate
from django.db.models import Count, Avg

categories = Category.objects.annotate(
    listing_count=Count('listings')
).filter(listing_count__gt=0)
```

**Beneficii:**
- Reducere semnificativă a numărului de query-uri
- Performanță îmbunătățită la scară mare
- Utilizare mai eficientă a resurselor DB

## 5. Documentație Tehnică Suplimentară

**Recomandări:**
1. Adăugare docstring-uri conforme cu PEP 257
```python
def calculate_listing_score(listing):
    """Calculează scorul unui anunț pe baza multiple criterii.
    
    Args:
        listing (Listing): Instanța de Listing pentru care se calculează scorul
        
    Returns:
        float: Scorul calculat între 0 și 100
    """
    # Implementare
```

2. Generare documentație API automată cu drf-yasg sau drf-spectacular
3. Diagrame arhitecturale în format Mermaid pentru:
   - Flow-uri de date
   - Relații între componente
   - Secvențe de apeluri

**Beneficii:**
- Mai ușor de întreținut codul
- Onboarding mai rapid pentru noii dezvoltatori
- Transparență în design-ul sistemului