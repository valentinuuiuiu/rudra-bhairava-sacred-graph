#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
sys.path.append('/home/shiva/Desktop/piata-ro-project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'piata_ro.settings')
django.setup()

from marketplace.models import CreditPackage
from decimal import Decimal

# Create credit packages
packages = [
    {
        'name': 'Pachet Basic',
        'credits': Decimal('5.0'),
        'price_eur': Decimal('5.00'),
        'price_ron': Decimal('25.00'),
        'description': '5 credite pentru 10 promovări',
        'is_active': True
    },
    {
        'name': 'Pachet Premium',
        'credits': Decimal('20.0'),
        'price_eur': Decimal('20.00'),
        'price_ron': Decimal('100.00'),
        'description': '20 credite pentru 40 promovări',
        'is_active': True
    },
    {
        'name': 'Pachet Starter',
        'credits': Decimal('1.0'),
        'price_eur': Decimal('1.00'),
        'price_ron': Decimal('5.00'),
        'description': '1 credit pentru 2 promovări',
        'is_active': True
    }
]

print("Creating credit packages...")
for package_data in packages:
    package, created = CreditPackage.objects.get_or_create(
        name=package_data['name'],
        defaults=package_data
    )
    if created:
        print(f"✅ Created: {package.name} - {package.credits} credite - {package.price_eur}€")
    else:
        print(f"⚠️  Already exists: {package.name}")

print("\n📊 Current packages:")
for package in CreditPackage.objects.all():
    print(f"- {package.name}: {package.credits} credite = {package.price_eur}€ / {package.price_ron} RON")

print("\n🎉 Credit packages setup complete!")
