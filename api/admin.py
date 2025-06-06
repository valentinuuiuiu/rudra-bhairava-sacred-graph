from django.contrib import admin
from .models import Category, Listing, Message, Favorite, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'currency', 'location', 'user', 'category', 'status', 'created_at')
    list_filter = ('status', 'is_premium', 'is_verified', 'category')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'created_at'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'listing', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('content', 'sender__username', 'receiver__username')
    date_hierarchy = 'created_at'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'listing__title')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'is_premium', 'premium_until')
    list_filter = ('is_premium',)
    search_fields = ('user__username', 'user__email', 'location')
