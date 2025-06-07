from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import asyncio
import httpx
from datetime import datetime

from .models import Category, Favorite, Listing, Message, UserProfile, ListingReport
from .models_chat import ChatConversation, ChatMessage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "price",
        "currency",
        "location",
        "user",
        "category",
        "status",
        "created_at",
    )
    list_filter = ("status", "is_premium", "is_verified", "category")
    search_fields = ("title", "description", "location")
    date_hierarchy = "created_at"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "listing", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("content", "sender__username", "receiver__username")
    date_hierarchy = "created_at"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "listing__title")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "location", "is_premium", "premium_until")
    list_filter = ("is_premium",)
    search_fields = ("user__username", "user__email", "phone", "location")


@admin.register(ListingReport)
class ListingReportAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "reporter", "reason", "status", "created_at")
    list_filter = ("reason", "status", "created_at")
    search_fields = ("listing__title", "reporter__username", "comment")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)

    fieldsets = (
        (None, {"fields": ("listing", "reporter", "reason", "comment")}),
        (
            "Status",
            {"fields": ("status", "reviewed_by", "reviewed_at", "notes")},
        ),
        ("Timestamps", {"fields": ("created_at",)}),
    )

    def save_model(self, request, obj, form, change):
        if change and obj.status in ["reviewed", "resolved", "dismissed"]:
            if not obj.reviewed_by:
                obj.reviewed_by = request.user
            if not obj.reviewed_at:
                from django.utils import timezone

                obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)
