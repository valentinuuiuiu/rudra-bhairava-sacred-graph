from django.contrib.auth.models import User
from rest_framework import serializers

from marketplace.models import Category, Favorite, Listing, Message, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "date_joined"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ["user", "avatar", "bio", "phone", "location", "is_premium"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "icon", "color", "parent"]


class ListingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = CategorySerializer(read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "price",
            "currency",
            "location",
            "images",
            "user",
            "category",
            "subcategory",
            "status",
            "created_at",
            "updated_at",
            "expires_at",
            "is_premium",
            "views",
            "metadata",
            "is_verified",
        ]
        read_only_fields = ["user", "views", "is_verified", "created_at", "updated_at"]


class ListingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "price",
            "currency",
            "location",
            "images",
            "category",
            "subcategory",
        ]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "receiver",
            "listing",
            "content",
            "created_at",
            "is_read",
        ]
        read_only_fields = ["sender", "created_at"]


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["receiver", "listing", "content"]

    def create(self, validated_data):
        validated_data["sender"] = self.context["request"].user
        return super().create(validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "user", "listing", "created_at"]
        read_only_fields = ["user", "created_at"]


class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["listing"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
