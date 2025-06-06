from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Category, Favorite, Listing, Message, UserProfile, ListingImage
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
from .forms import ListingForm, CustomUserCreationForm


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


# Frontend Views for the Comprehensive Marketplace

def home_view(request):
    """Homepage view with enhanced functionality."""
    # Get all categories for the dropdown
    categories = Category.objects.all()

    # Get featured/promoted listings
    featured_listings = Listing.objects.filter(
        status="active", is_featured=True
    ).order_by("-created_at")[:8]

    # Get recent listings
    recent_listings = Listing.objects.filter(status="active").order_by("-created_at")[:12]

    # Get statistics
    total_listings = Listing.objects.filter(status="active").count()
    total_categories = Category.objects.count()

    context = {
        "categories": categories,
        "featured_listings": featured_listings,
        "recent_listings": recent_listings,
        "total_listings": total_listings,
        "total_categories": total_categories,
    }

    return render(request, "marketplace/index.html", context)


def categories_view(request):
    """Categories listing page."""
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
    
    context = {
        "categories": categories,
        "page_title": "Toate categoriile",
    }
    
    return render(request, "marketplace/categories.html", context)


def category_detail_view(request, category_slug):
    """Category detail page with listings."""
    from django.shortcuts import get_object_or_404
    
    category = get_object_or_404(Category, slug=category_slug)
    
    # Get subcategories
    subcategories = Category.objects.filter(parent=category)
    
    # Get listings in this category and subcategories
    category_ids = [category.id] + list(subcategories.values_list('id', flat=True))
    listings = Listing.objects.filter(
        category_id__in=category_ids,
        status="active"
    ).order_by("-created_at")
    
    # Handle pagination
    from django.core.paginator import Paginator
    paginator = Paginator(listings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "category": category,
        "subcategories": subcategories,
        "listings": page_obj,
        "page_title": f"Categoria: {category.name}",
    }
    
    return render(request, "marketplace/category_detail.html", context)


def listings_view(request):
    """All listings page with filtering."""
    listings = Listing.objects.filter(status="active").order_by("-created_at")
    categories = Category.objects.all()
    
    # Apply filters
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    location = request.GET.get('location', '')
    
    if search_query:
        listings = listings.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if category_id:
        listings = listings.filter(category_id=category_id)
    
    if min_price:
        try:
            listings = listings.filter(price__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            listings = listings.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    if location:
        listings = listings.filter(location__icontains=location)
    
    # Handle pagination
    from django.core.paginator import Paginator
    paginator = Paginator(listings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "listings": page_obj,
        "categories": categories,
        "search_query": search_query,
        "selected_category": category_id,
        "min_price": min_price,
        "max_price": max_price,
        "location": location,
        "page_title": "Toate anunțurile",
    }
    
    return render(request, "marketplace/listings.html", context)


def listing_detail_view(request, listing_id):
    """Listing detail page."""
    from django.shortcuts import get_object_or_404
    
    listing = get_object_or_404(Listing, id=listing_id, status="active")
    
    # Increment views
    listing.views += 1
    listing.save(update_fields=['views'])
    
    # Get related listings
    related_listings = Listing.objects.filter(
        category=listing.category,
        status="active"
    ).exclude(id=listing.id)[:6]
    
    context = {
        "listing": listing,
        "related_listings": related_listings,
        "page_title": listing.title,
    }
    
    return render(request, "marketplace/listing_detail.html", context)


def add_listing_view(request):
    """Add new listing page."""
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.status = 'active'  # Set to active by default
            listing.save()
            
            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                ListingImage.objects.create(
                    listing=listing,
                    image=image,
                    is_primary=(i == 0)  # First image is primary
                )
            
            messages.success(request, 'Anunțul a fost creat cu succes!')
            return redirect('marketplace:listing_detail', listing_id=listing.id)
        else:
            messages.error(request, 'Te rugăm să corectezi erorile de mai jos.')
    else:
        form = ListingForm()
    
    categories = Category.objects.filter(parent__isnull=True)
    
    context = {
        "form": form,
        "categories": categories,
        "page_title": "Adaugă anunț nou",
    }
    
    return render(request, "marketplace/add_listing.html", context)


def profile_view(request):
    """User profile page."""
    from django.contrib.auth.decorators import login_required
    from django.shortcuts import redirect
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    user_listings = Listing.objects.filter(user=request.user).order_by("-created_at")
    
    context = {
        "user_listings": user_listings,
        "page_title": "Profilul meu",
    }
    
    return render(request, "marketplace/profile.html", context)


def messages_view(request):
    """Messages page."""
    from django.shortcuts import redirect
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get messages for current user
    received_messages = Message.objects.filter(receiver=request.user).order_by("-created_at")
    sent_messages = Message.objects.filter(sender=request.user).order_by("-created_at")
    
    context = {
        "received_messages": received_messages,
        "sent_messages": sent_messages,
        "page_title": "Mesajele mele",
    }
    
    return render(request, "marketplace/messages.html", context)


def favorites_view(request):
    """Favorites page."""
    from django.shortcuts import redirect
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    favorites = Favorite.objects.filter(user=request.user).select_related('listing')
    
    context = {
        "favorites": favorites,
        "page_title": "Favoritele mele",
    }
    
    return render(request, "marketplace/favorites.html", context)


def search_view(request):
    """Search results page."""
    query = request.GET.get('q', '')
    categories = Category.objects.all()
    
    listings = Listing.objects.none()
    
    if query:
        listings = Listing.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(location__icontains=query),
            status="active"
        ).order_by("-created_at")
    
    # Handle pagination
    from django.core.paginator import Paginator
    paginator = Paginator(listings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "listings": page_obj,
        "query": query,
        "categories": categories,
        "page_title": f"Căutare: {query}" if query else "Căutare",
    }
    
    return render(request, "marketplace/search.html", context)


def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Contul pentru {username} a fost creat cu succes!')
            login(request, user)
            return redirect('marketplace:home')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})
