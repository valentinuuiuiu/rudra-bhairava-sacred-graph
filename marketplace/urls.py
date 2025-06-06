from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'marketplace'

# API Router for REST endpoints
router = DefaultRouter()
router.register(r"categories", views.CategoryViewSet)
router.register(r"listings", views.ListingViewSet)
router.register(r"messages", views.MessageViewSet)
router.register(r"favorites", views.FavoriteViewSet)
router.register(r"users", views.UserProfileViewSet)

urlpatterns = [
    # Frontend pages
    path('', views.home_view, name='home'),
    path('categorii/', views.categories_view, name='categories'),
    path('categorii/<slug:category_slug>/', views.category_detail_view, name='category_detail'),
    path('anunturi/', views.listings_view, name='listings'),
    path('anunt/<int:listing_id>/', views.listing_detail_view, name='listing_detail'),
    path('adauga-anunt/', views.add_listing_view, name='add_listing'),
    path('profil/', views.profile_view, name='profile'),
    path('mesaje/', views.messages_view, name='messages'),
    path('favorite/', views.favorites_view, name='favorites'),
    path('cautare/', views.search_view, name='search'),
    
    # API endpoints (keeping existing structure)
    path("api/", include(router.urls)),
]
