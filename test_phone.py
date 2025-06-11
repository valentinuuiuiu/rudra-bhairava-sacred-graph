#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'piata_ro.settings')
django.setup()

from django.contrib.auth.models import User
from marketplace.models import UserProfile

# Let's add a test phone number to the admin user
admin_user = User.objects.get(username='admin')
profile = admin_user.profile
profile.phone = '0723456789'
profile.save()

print(f"Added phone number {profile.phone} to user {admin_user.username}")

# Verify it was saved
profile.refresh_from_db()
print(f"Verified: Phone number is now {profile.phone}")
