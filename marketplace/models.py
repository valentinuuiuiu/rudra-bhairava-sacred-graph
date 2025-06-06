from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subcategories",
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def listing_image_path(instance, filename):
    # Generate path like: listings/user_id/listing_id/image.jpg
    return f"listings/{instance.listing.user.id}/{instance.listing.id}/{filename}"


class Listing(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("active", "Active"),
        ("sold", "Sold"),
        ("expired", "Expired"),
        ("rejected", "Rejected"),
    )
    
    CURRENCY_CHOICES = (
        ("RON", "Lei (RON)"),
        ("EUR", "Euro (EUR)"),
        ("USD", "Dolari (USD)"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, default="RON", choices=CURRENCY_CHOICES)
    location = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="listings"
    )
    subcategory = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="subcategory_listings",
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    metadata = models.JSONField(blank=True, null=True)  # For additional attributes
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["category", "status"]),
            models.Index(fields=["user", "status"]),
        ]

    def __str__(self):
        return self.title

    @property
    def main_image(self):
        image = self.images.filter(is_main=True).first()
        if not image:
            image = self.images.first()
        return image


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=listing_image_path)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def save(self, *args, **kwargs):
        if self.is_main:
            # Ensure only one main image per listing
            ListingImage.objects.filter(listing=self.listing).update(is_main=False)
        super().save(*args, **kwargs)


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="messages",
        blank=True,
        null=True,
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "listing")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} favorited {self.listing.title}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    premium_until = models.DateTimeField(blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
