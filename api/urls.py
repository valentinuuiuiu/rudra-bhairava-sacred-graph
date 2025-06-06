from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"categories", views.CategoryViewSet)
router.register(r"listings", views.ListingViewSet)
router.register(r"messages", views.MessageViewSet)
router.register(r"favorites", views.FavoriteViewSet)
router.register(r"users", views.UserProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
