from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from marketplace.models import Category, Listing
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **options):
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )

        if created:
            user.set_password('testpassword')
            user.save()
            self.stdout.write(f'Created test user: {user.username}')

        # Sample listings data
        listings_data = [
            # Cars
            {
                'title': 'BMW X5 2019 - Impecabil',
                'description': 'BMW X5 în stare perfectă, second hand, cu toate opțiunile. Motor diesel, consum redus.',
                'price': Decimal('45000'),
                'location': 'București',
                'category_slug': 'used-cars',
                'is_featured': True
            },
            {
                'title': 'Toyota RAV4 Hybrid 2021',
                'description': 'SUV hibrid, economic și spațios. Perfect pentru familie.',
                'price': Decimal('38000'),
                'location': 'Cluj-Napoca',
                'category_slug': 'used-cars'
            },
            {
                'title': 'Yamaha MT-07 2020',
                'description': 'Motocicletă sport, puțin folosită, în garanție.',
                'price': Decimal('8500'),
                'location': 'Timișoara',
                'category_slug': 'motorcycles'
            },

            # Electronics
            {
                'title': 'iPhone 14 Pro Max 256GB',
                'description': 'Telefon nou, nedespachet, cu toate accesoriile incluse.',
                'price': Decimal('5500'),
                'location': 'București',
                'category_slug': 'mobile-phones',
                'is_featured': True
            },
            {
                'title': 'Laptop Gaming ASUS ROG',
                'description': 'Laptop pentru gaming, RTX 4060, 16GB RAM, SSD 1TB.',
                'price': Decimal('7200'),
                'location': 'Iași',
                'category_slug': 'computers'
            },
            {
                'title': 'PlayStation 5 + 2 Controller-e',
                'description': 'Consolă PS5 cu două controller-e și 3 jocuri incluse.',
                'price': Decimal('2800'),
                'location': 'Constanța',
                'category_slug': 'gaming'
            },

            # Real Estate
            {
                'title': 'Apartament 3 camere Herastrău',
                'description': 'Apartament modern, recent renovat, parcare subterană inclusă.',
                'price': Decimal('180000'),
                'location': 'București, Herastrău',
                'category_slug': 'apartments-sale',
                'is_featured': True
            },
            {
                'title': 'Casă cu grădină în Bragadiru',
                'description': 'Casă individuală cu grădină mare, 4 camere, garaj.',
                'price': Decimal('150000'),
                'location': 'Bragadiru',
                'category_slug': 'houses-sale'
            },
            {
                'title': 'Apartament de închiriat 2 camere',
                'description': 'Apartament mobilat complet, zona centrală.',
                'price': Decimal('800'),
                'location': 'Cluj-Napoca',
                'category_slug': 'apartments-rent'
            },

            # Jobs
            {
                'title': 'Dezvoltator Python Senior',
                'description': 'Căutăm dezvoltator Python cu experiență în Django și FastAPI.',
                'price': Decimal('8000'),
                'location': 'București (Remote)',
                'category_slug': 'it-technology'
            },
            {
                'title': 'Manager Vânzări Regional',
                'description': 'Poziție de manager pentru echipa de vânzări din regiunea Vest.',
                'price': Decimal('5500'),
                'location': 'Timișoara',
                'category_slug': 'sales-marketing'
            },

            # Services
            {
                'title': 'Servicii Renovări Complete',
                'description': 'Oferim servicii complete de renovare pentru apartamente și case.',
                'price': Decimal('50'),
                'location': 'București',
                'category_slug': 'home-services'
            },
            {
                'title': 'Frizerie și Salon de Înfrumusețare',
                'description': 'Servicii complete de frizerie și cosmetică.',
                'price': Decimal('80'),
                'location': 'Cluj-Napoca',
                'category_slug': 'beauty-wellness'
            },

            # Fashion
            {
                'title': 'Rochie de Seară Designer',
                'description': 'Rochie elegantă pentru evenimente speciale, mărimea M.',
                'price': Decimal('350'),
                'location': 'București',
                'category_slug': 'womens-clothing'
            },
            {
                'title': 'Costum Bărbătesc Hugo Boss',
                'description': 'Costum elegant, perfect pentru evenimente business.',
                'price': Decimal('800'),
                'location': 'Cluj-Napoca',
                'category_slug': 'mens-clothing'
            },

            # Sports
            {
                'title': 'Bicicletă Montain Bike Trek',
                'description': 'Bicicletă profesională pentru trasee montane.',
                'price': Decimal('2200'),
                'location': 'Brașov',
                'category_slug': 'sports-gear'
            },
            {
                'title': 'Set Gantere Reglabile',
                'description': 'Set complet pentru antrenament acasă, 2x20kg.',
                'price': Decimal('450'),
                'location': 'București',
                'category_slug': 'fitness-equipment'
            }
        ]

        self.stdout.write('Starting listings seeding...')

        for listing_data in listings_data:
            try:
                # Get the category
                category = Category.objects.get(slug=listing_data['category_slug'])
                
                # Check if listing already exists
                existing = Listing.objects.filter(
                    title=listing_data['title'],
                    user=user
                ).exists()

                if not existing:
                    listing = Listing.objects.create(
                        title=listing_data['title'],
                        description=listing_data['description'],
                        price=listing_data['price'],
                        location=listing_data['location'],
                        category=category,
                        user=user,
                        status='active',
                        is_featured=listing_data.get('is_featured', False)
                    )
                    self.stdout.write(f'Created listing: {listing.title}')
                else:
                    self.stdout.write(f'Listing already exists: {listing_data["title"]}')

            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Category not found: {listing_data["category_slug"]}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating listing {listing_data["title"]}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded listings!')
        )
