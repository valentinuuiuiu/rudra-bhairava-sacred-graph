from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from marketplace.models import Category, Listing
from decimal import Decimal
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Populate database with Romanian categories and sample listings'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Romanian data population...'))
        
        # Clear existing data
        self.stdout.write('Clearing existing categories and listings...')
        Listing.objects.all().delete()
        Category.objects.all().delete()
        
        # Create main categories
        self.stdout.write('Creating main categories...')
        main_categories = [
            {'name': 'Imobiliare', 'slug': 'imobiliare', 'icon': 'fas fa-home', 'color': '#4CAF50'},
            {'name': 'Auto, Moto și Ambarcațiuni', 'slug': 'auto-moto-ambarcatiuni', 'icon': 'fas fa-car', 'color': '#2196F3'},
            {'name': 'Electronice și Electrocasnice', 'slug': 'electronice-electrocasnice', 'icon': 'fas fa-laptop', 'color': '#FF9800'},
            {'name': 'Locuri de Muncă', 'slug': 'locuri-de-munca', 'icon': 'fas fa-briefcase', 'color': '#9C27B0'},
            {'name': 'Servicii, Afaceri, Echipamente Firme', 'slug': 'servicii-afaceri-echipamente', 'icon': 'fas fa-concierge-bell', 'color': '#3F51B5'},
            {'name': 'Modă și Frumusețe', 'slug': 'moda-frumusete', 'icon': 'fas fa-tshirt', 'color': '#E91E63'},
            {'name': 'Casă și Grădină', 'slug': 'casa-gradina', 'icon': 'fas fa-leaf', 'color': '#8BC34A'},
            {'name': 'Sport, Timp Liber, Artă', 'slug': 'sport-timp-liber-arta', 'icon': 'fas fa-futbol', 'color': '#FFC107'},
            {'name': 'Mama și Copilul', 'slug': 'mama-copilul', 'icon': 'fas fa-child', 'color': '#00BCD4'},
            {'name': 'Animale de Companie', 'slug': 'animale-companie', 'icon': 'fas fa-paw', 'color': '#607D8B'},
            {'name': 'Agro și Industrie', 'slug': 'agro-industrie', 'icon': 'fas fa-tractor', 'color': '#795548'},
        ]
        
        created_main_categories = {}
        for cat_data in main_categories:
            category = Category.objects.create(**cat_data)
            created_main_categories[cat_data['name']] = category
            self.stdout.write(f'Created main category: {category.name}')
        
        # Create subcategories
        self.stdout.write('Creating subcategories...')
        subcategories_data = [
            # Imobiliare subcategories
            {'name': 'Apartamente de vânzare', 'slug': 'apartamente-vanzare', 'icon': 'far fa-building', 'color': '#4CAF50', 'parent': 'Imobiliare'},
            {'name': 'Apartamente de închiriat', 'slug': 'apartamente-inchiriat', 'icon': 'far fa-building', 'color': '#4CAF50', 'parent': 'Imobiliare'},
            {'name': 'Case de vânzare', 'slug': 'case-vanzare', 'icon': 'fas fa-home', 'color': '#4CAF50', 'parent': 'Imobiliare'},
            {'name': 'Case de închiriat', 'slug': 'case-inchiriat', 'icon': 'fas fa-home', 'color': '#4CAF50', 'parent': 'Imobiliare'},
            {'name': 'Terenuri', 'slug': 'terenuri', 'icon': 'fas fa-map-marked-alt', 'color': '#4CAF50', 'parent': 'Imobiliare'},
            {'name': 'Spații comerciale/Birouri', 'slug': 'spatii-comerciale-birouri', 'icon': 'fas fa-store', 'color': '#4CAF50', 'parent': 'Imobiliare'},
            {'name': 'Cazare/Turism', 'slug': 'cazare-turism', 'icon': 'fas fa-hotel', 'color': '#4CAF50', 'parent': 'Imobiliare'},
            
            # Auto, Moto și Ambarcațiuni subcategories
            {'name': 'Autoturisme', 'slug': 'autoturisme', 'icon': 'fas fa-car-side', 'color': '#2196F3', 'parent': 'Auto, Moto și Ambarcațiuni'},
            {'name': 'Motociclete/Scutere/ATV', 'slug': 'moto-scutere-atv', 'icon': 'fas fa-motorcycle', 'color': '#2196F3', 'parent': 'Auto, Moto și Ambarcațiuni'},
            {'name': 'Rulote/Autorulote', 'slug': 'rulote-autorulote', 'icon': 'fas fa-caravan', 'color': '#2196F3', 'parent': 'Auto, Moto și Ambarcațiuni'},
            {'name': 'Camioane/Utilaje', 'slug': 'camioane-utilaje', 'icon': 'fas fa-truck', 'color': '#2196F3', 'parent': 'Auto, Moto și Ambarcațiuni'},
            {'name': 'Ambarcațiuni', 'slug': 'ambarcatiuni', 'icon': 'fas fa-ship', 'color': '#2196F3', 'parent': 'Auto, Moto și Ambarcațiuni'},
            {'name': 'Piese Auto', 'slug': 'piese-auto', 'icon': 'fas fa-cogs', 'color': '#2196F3', 'parent': 'Auto, Moto și Ambarcațiuni'},
            {'name': 'Servicii Auto', 'slug': 'servicii-auto', 'icon': 'fas fa-tools', 'color': '#2196F3', 'parent': 'Auto, Moto și Ambarcațiuni'},
            
            # Electronice și Electrocasnice subcategories
            {'name': 'Telefoane', 'slug': 'telefoane', 'icon': 'fas fa-mobile-alt', 'color': '#FF9800', 'parent': 'Electronice și Electrocasnice'},
            {'name': 'Calculatoare/Laptopuri', 'slug': 'calculatoare-laptopuri', 'icon': 'fas fa-laptop', 'color': '#FF9800', 'parent': 'Electronice și Electrocasnice'},
            {'name': 'TV/Audio/Video', 'slug': 'tv-audio-video', 'icon': 'fas fa-tv', 'color': '#FF9800', 'parent': 'Electronice și Electrocasnice'},
            {'name': 'Electrocasnice Mari', 'slug': 'electrocasnice-mari', 'icon': 'fas fa-blender', 'color': '#FF9800', 'parent': 'Electronice și Electrocasnice'},
            {'name': 'Electrocasnice Mici', 'slug': 'electrocasnice-mici', 'icon': 'fas fa-coffee', 'color': '#FF9800', 'parent': 'Electronice și Electrocasnice'},
            {'name': 'Jocuri/Console', 'slug': 'jocuri-console', 'icon': 'fas fa-gamepad', 'color': '#FF9800', 'parent': 'Electronice și Electrocasnice'},
            {'name': 'Aparate Foto/Video', 'slug': 'aparate-foto-video', 'icon': 'fas fa-camera-retro', 'color': '#FF9800', 'parent': 'Electronice și Electrocasnice'},
            
            # Modă și Frumusețe subcategories
            {'name': 'Haine Damă', 'slug': 'haine-dama', 'icon': 'fas fa-female', 'color': '#E91E63', 'parent': 'Modă și Frumusețe'},
            {'name': 'Haine Bărbați', 'slug': 'haine-barbati', 'icon': 'fas fa-male', 'color': '#E91E63', 'parent': 'Modă și Frumusețe'},
            {'name': 'Haine Copii', 'slug': 'haine-copii', 'icon': 'fas fa-child', 'color': '#E91E63', 'parent': 'Modă și Frumusețe'},
            {'name': 'Încălțăminte', 'slug': 'incaltaminte', 'icon': 'fas fa-shoe-prints', 'color': '#E91E63', 'parent': 'Modă și Frumusețe'},
            {'name': 'Accesorii (Genți, Ceasuri, Bijuterii)', 'slug': 'accesorii-genti-ceasuri-bijuterii', 'icon': 'fas fa-gem', 'color': '#E91E63', 'parent': 'Modă și Frumusețe'},
            {'name': 'Cosmetice/Parfumuri', 'slug': 'cosmetice-parfumuri', 'icon': 'fas fa-magic', 'color': '#E91E63', 'parent': 'Modă și Frumusețe'},
        ]
        
        created_subcategories = {}
        for subcat_data in subcategories_data:
            parent_name = subcat_data.pop('parent')
            parent_category = created_main_categories[parent_name]
            subcategory = Category.objects.create(parent=parent_category, **subcat_data)
            created_subcategories[subcategory.name] = subcategory
            self.stdout.write(f'Created subcategory: {subcategory.name} under {parent_category.name}')
        
        # Create sample users
        self.stdout.write('Creating sample users...')
        users_data = [
            {'username': 'admin', 'email': 'admin@piata.ro', 'first_name': 'Admin', 'last_name': 'User'},
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'alex_popescu', 'email': 'alex@example.com', 'first_name': 'Alex', 'last_name': 'Popescu'},
            {'username': 'maria_ionescu', 'email': 'maria@example.com', 'first_name': 'Maria', 'last_name': 'Ionescu'},
        ]
        
        created_users = {}
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password('password123')  # Set a default password
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            else:
                self.stdout.write(f'User already exists: {user.username}')
            created_users[user.username] = user
        
        # Create sample listings
        self.stdout.write('Creating sample listings...')
        listings_data = [
            {
                'title': 'Apartament modern 2 camere în centrul Bucureștiului',
                'description': 'Apartament frumos, recent renovat cu 2 dormitoare, living, bucătărie și baie. Situat în inima Bucureștiului, aproape de toate facilitățile.',
                'price': Decimal('120000'),
                'currency': 'EUR',
                'location': 'Bucuresti, Sector 1',
                'images': ['https://images.unsplash.com/photo-1522708323590-d24dbb6b0267', 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688'],
                'user': 'john_doe',
                'category': 'Imobiliare',
                'subcategory': 'Apartamente de vânzare',
                'status': 'active',
                'is_premium': True,
                'views': 156,
            },
            {
                'title': 'BMW 320d 2018, stare excelentă',
                'description': 'Vând BMW 320d din 2018 cu 75.000 km. Istoric complet de service, fără accidente, un singur proprietar. Diesel, transmisie automată, scaune din piele, navigație.',
                'price': Decimal('22500'),
                'currency': 'EUR',
                'location': 'Cluj-Napoca',
                'images': ['https://images.unsplash.com/photo-1555215695-3004980ad54e', 'https://images.unsplash.com/photo-1520031441872-956195f7e400'],
                'user': 'alex_popescu',
                'category': 'Auto, Moto și Ambarcațiuni',
                'subcategory': 'Autoturisme',
                'status': 'active',
                'is_premium': True,
                'views': 243,
            },
            {
                'title': 'iPhone 13 Pro, 256GB, ca nou',
                'description': 'Vând iPhone 13 Pro, 256GB, culoare graphite. Folosit 6 luni, stare ca nou, fără zgârieturi. Vine cu cutia originală, încărcător și husă.',
                'price': Decimal('3500'),
                'currency': 'RON',
                'location': 'Timisoara',
                'images': ['https://images.unsplash.com/photo-1632661674596-618e45e68f10'],
                'user': 'jane_smith',
                'category': 'Electronice și Electrocasnice',
                'subcategory': 'Telefoane',
                'status': 'active',
                'is_premium': False,
                'views': 87,
            },
            {
                'title': 'Dezvoltator Software - Lucru Remote',
                'description': 'Căutăm un dezvoltator software experimentat să se alăture echipei noastre. Lucru remote posibil. Cerințe: 3+ ani experiență cu JavaScript, React, Node.js.',
                'price': None,
                'currency': 'RON',
                'location': 'Remote',
                'images': [],
                'user': 'maria_ionescu',
                'category': 'Locuri de Muncă',
                'subcategory': None,
                'status': 'active',
                'is_premium': True,
                'views': 312,
            },
            {
                'title': 'Servicii profesionale de curățenie locuințe',
                'description': 'Oferim servicii profesionale de curățenie locuințe în Brașov. Curățenie regulată, generală, mutări. Experiență, încredere și prețuri accesibile.',
                'price': Decimal('150'),
                'currency': 'RON',
                'location': 'Brasov',
                'images': ['https://images.unsplash.com/photo-1581578731548-c64695cc6952'],
                'user': 'alex_popescu',
                'category': 'Servicii, Afaceri, Echipamente Firme',
                'subcategory': None,
                'status': 'active',
                'is_premium': False,
                'views': 45,
            },
            {
                'title': 'Jachetă din piele designer, mărimea M',
                'description': 'Vând o jachetă frumoasă din piele de designer, mărimea M. Culoare neagră, stare excelentă, purtată doar de câteva ori. Prețul original 2000 RON.',
                'price': Decimal('1200'),
                'currency': 'RON',
                'location': 'Constanta',
                'images': ['https://images.unsplash.com/photo-1551028719-00167b16eac5'],
                'user': 'maria_ionescu',
                'category': 'Modă și Frumusețe',
                'subcategory': 'Haine Damă',
                'status': 'active',
                'is_premium': False,
                'views': 67,
            },
            {
                'title': 'Set mobilier grădină',
                'description': 'Vând set mobilier grădină: masă și 4 scaune. Făcut din lemn de calitate, rezistent la intemperii. Folosit un sezon, stare excelentă.',
                'price': Decimal('800'),
                'currency': 'RON',
                'location': 'Bucuresti, Sector 3',
                'images': ['https://images.unsplash.com/photo-1595429035839-c99c298ffdde'],
                'user': 'john_doe',
                'category': 'Casă și Grădină',
                'subcategory': None,
                'status': 'active',
                'is_premium': False,
                'views': 34,
            },
            {
                'title': 'Bicicletă montană - Trek Marlin 7',
                'description': 'Vând bicicleta mea de munte Trek Marlin 7. Mărimea L, roți 29", frâne pe disc hidraulice. Folosită un sezon, stare excelentă.',
                'price': Decimal('2500'),
                'currency': 'RON',
                'location': 'Cluj-Napoca',
                'images': ['https://images.unsplash.com/photo-1576435728678-68d0fbf94e91'],
                'user': 'jane_smith',
                'category': 'Sport, Timp Liber, Artă',
                'subcategory': None,
                'status': 'active',
                'is_premium': True,
                'views': 128,
            },
        ]
        
        for listing_data in listings_data:
            user_key = listing_data.pop('user')
            category_key = listing_data.pop('category')
            subcategory_key = listing_data.pop('subcategory', None)
            
            user = created_users[user_key]
            category = created_main_categories[category_key]
            subcategory = created_subcategories.get(subcategory_key) if subcategory_key else None
            
            listing = Listing.objects.create(
                user=user,
                category=category,
                subcategory=subcategory,
                **listing_data
            )
            self.stdout.write(f'Created listing: {listing.title}')
        
        self.stdout.write(self.style.SUCCESS('Romanian data population completed successfully!'))
        self.stdout.write(f'Created {Category.objects.count()} categories and {Listing.objects.count()} listings')
