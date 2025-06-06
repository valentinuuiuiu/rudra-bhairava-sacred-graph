from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Favorite, Listing, Message, UserProfile
from .serializers import (
    CategorySerializer,
    FavoriteCreateSerializer,
    FavoriteSerializer,
    ListingCreateSerializer,
    ListingSerializer,
    MessageCreateSerializer,
    MessageSerializer,
    UserProfileSerializer,
    UserSerializer,
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        if hasattr(obj, "user"):
            return obj.user == request.user
        elif hasattr(obj, "sender"):
            return obj.sender == request.user
        return False


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    @action(detail=True, methods=["get"])
    def subcategories(self, request, pk=None):
        category = self.get_object()
        subcategories = Category.objects.filter(parent=category)
        serializer = self.get_serializer(subcategories, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def listings(self, request, pk=None):
        category = self.get_object()
        listings = Listing.objects.filter(
            Q(category=category) | Q(subcategory=category), status="active"
        )
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "location"]
    ordering_fields = ["created_at", "price", "views"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Listing.objects.all()

        # Filter by status (default to active)
        status = self.request.query_params.get("status", "active")
        if status != "all":
            queryset = queryset.filter(status=status)

        # Filter by category
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(
                Q(category_id=category_id) | Q(subcategory_id=category_id)
            )

        # Filter by price range
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Filter by location
        location = self.request.query_params.get("location")
        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ListingCreateSerializer
        return ListingSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.views += 1
        instance.save(update_fields=["views"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def favorite(self, request, pk=None):
        listing = self.get_object()
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        favorite, created = Favorite.objects.get_or_create(user=user, listing=listing)

        if created:
            return Response(
                {"detail": "Listing added to favorites"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"detail": "Listing already in favorites"}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def unfavorite(self, request, pk=None):
        listing = self.get_object()
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            favorite = Favorite.objects.get(user=user, listing=listing)
            favorite.delete()
            return Response(
                {"detail": "Listing removed from favorites"}, status=status.HTTP_200_OK
            )
        except Favorite.DoesNotExist:
            return Response(
                {"detail": "Listing not in favorites"}, status=status.HTTP_404_NOT_FOUND
            )


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(receiver=user))

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return MessageCreateSerializer
        return MessageSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return FavoriteCreateSerializer
        return FavoriteSerializer


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["get"])
    def listings(self, request, pk=None):
        user = self.get_object()
        listings = Listing.objects.filter(user=user, status="active")
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def profile(self, request, pk=None):
        user = self.get_object()
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)

        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


def home(request):
    """Homepage view."""
    # Get all categories for the dropdown
    categories = Category.objects.all()

    # Get featured/promoted listings
    featured_listings = Listing.objects.filter(
        status="active", is_featured=True
    ).order_by("-created_at")[:8]

    # Get recent listings
    recent_listings = Listing.objects.filter(status="active").order_by("-created_at")[
        :8
    ]

    context = {
        "categories": categories,
        "featured_listings": featured_listings,
        "recent_listings": recent_listings,
    }

    return render(request, "marketplace/index.html", context)
