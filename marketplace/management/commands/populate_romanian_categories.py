from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from marketplace.models import Category, Listing
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Populate database with Romanian categories based on OLX.ro and Publi24.ro'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate Romanian categories...'))
        
        # Clear existing categories
        Category.objects.all().delete()
        
        # Main categories with their icons and colors based on OLX.ro and Publi24.ro
        main_categories = [
            {
                'name': 'Auto, Moto și Ambarcațiuni',
                'icon': 'fas fa-car',
                'color': '#2196F3',
                'subcategories': [
                    'Autoturisme',
                    'Motociclete/Scutere/ATV',
                    'Piese auto',
                    'Rulote/Autorulote',
                    'Camioane/Utilaje',
                    'Ambarcațiuni',
                    'Servicii auto',
                ]
            },
            {
                'name': 'Imobiliare',
                'icon': 'fas fa-home',
                'color': '#4CAF50',
                'subcategories': [
                    'Apartamente de vânzare',
                    'Apartamente de închiriat',
                    'Case de vânzare',
                    'Case de închiriat',
                    'Terenuri',
                    'Spații comerciale/Birouri',
                    'Cazare/Turism',
                ]
            },
            {
                'name': 'Locuri de Muncă',
                'icon': 'fas fa-briefcase',
                'color': '#9C27B0',
                'subcategories': [
                    'Oferte de angajare',
                    'CV-uri/Cereri de angajare',
                    'Servicii de recrutare',
                    'Freelancing',
                    'Practică/Internship',
                ]
            },
            {
                'name': 'Electronice și Electrocasnice',
                'icon': 'fas fa-laptop',
                'color': '#FF9800',
                'subcategories': [
                    'Telefoane',
                    'Calculatoare/Laptopuri',
                    'TV/Audio/Video',
                    'Electrocasnice mari',
                    'Electrocasnice mici',
                    'Jocuri/Console',
                    'Aparate foto/Video',
                ]
            },
            {
                'name': 'Modă și Frumusețe',
                'icon': 'fas fa-tshirt',
                'color': '#E91E63',
                'subcategories': [
                    'Haine damă',
                    'Haine bărbați',
                    'Haine copii',
                    'Încălțăminte',
                    'Accesorii (Genți, Ceasuri, Bijuterii)',
                    'Cosmetice/Parfumuri',
                ]
            },
            {
                'name': 'Casă și Grădină',
                'icon': 'fas fa-leaf',
                'color': '#8BC34A',
                'subcategories': [
                    'Mobilă/Decorațiuni',
                    'Unelte/Materiale de construcții',
                    'Articole menaj/Curățenie',
                    'Plante/Amenajări grădină',
                    'Sisteme securitate/Alarme',
                ]
            },
            {
                'name': 'Mama și Copilul',
                'icon': 'fas fa-child',
                'color': '#00BCD4',
                'subcategories': [
                    'Cărucioare/Scaune auto',
                    'Haine/Încălțăminte copii',
                    'Jucării',
                    'Articole școlare',
                    'Articole bebeluși',
                ]
            },
            {
                'name': 'Sport, Timp Liber, Artă',
                'icon': 'fas fa-futbol',
                'color': '#FFC107',
                'subcategories': [
                    'Echipament sportiv',
                    'Biciclete',
                    'Echipament fitness',
                    'Instrumente muzicale',
                    'Cărți/Reviste',
                    'Hobby/Colecții',
                    'Turism/Călătorii',
                ]
            },
            {
                'name': 'Animale de Companie',
                'icon': 'fas fa-paw',
                'color': '#607D8B',
                'subcategories': [
                    'Câini',
                    'Pisici',
                    'Păsări',
                    'Hrană/Accesorii animale',
                    'Servicii veterinare',
                ]
            },
            {
                'name': 'Agro și Industrie',
                'icon': 'fas fa-tractor',
                'color': '#795548',
                'subcategories': [
                    'Utilaje agricole',
                    'Animale de fermă',
                    'Cereale/Semințe',
                    'Echipamente industriale',
                    'Materiale construcții',
                ]
            },
            {
                'name': 'Servicii',
                'icon': 'fas fa-concierge-bell',
                'color': '#3F51B5',
                'subcategories': [
                    'Servicii pentru casă',
                    'Servicii auto',
                    'Educație/Cursuri',
                    'Servicii medicale',
                    'Servicii juridice',
                    'Servicii IT',
                    'Servicii financiare',
                ]
            },
            {
                'name': 'Matrimoniale',
                'icon': 'fas fa-heart',
                'color': '#E91E63',
                'subcategories': [
                    'Bărbați caută femei',
                    'Femei caută bărbați',
                    'Prietenii',
                    'Servicii matrimoniale',
                ]
            }
        ]
        
        created_categories = 0
        created_subcategories = 0
        
        for category_data in main_categories:
            # Create main category
            main_category = Category.objects.create(
                name=category_data['name'],
                slug=slugify(category_data['name']),
                icon=category_data['icon'],
                color=category_data['color'],
                parent=None
            )
            created_categories += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Created main category: {main_category.name}')
            )
            
            # Create subcategories
            for subcat_name in category_data['subcategories']:
                # Create unique slug by combining parent slug and subcategory name
                unique_slug = f"{main_category.slug}-{slugify(subcat_name)}"
                subcategory = Category.objects.create(
                    name=subcat_name,
                    slug=unique_slug,
                    icon=category_data['icon'],  # Use same icon as parent
                    color=category_data['color'],  # Use same color as parent
                    parent=main_category
                )
                created_subcategories += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f'  - Created subcategory: {subcategory.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_categories} main categories '
                f'and {created_subcategories} subcategories!'
            )
        )
        
        # Create sample listings if there are users
        self.create_sample_listings()
    
    def create_sample_listings(self):
        """Create sample listings for the new categories"""
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(
                self.style.WARNING('No users found. Creating sample user...')
            )
            user = User.objects.create_user(
                username='demo_user',
                email='demo@piata.ro',
                password='demo123',
                first_name='Demo',
                last_name='User'
            )
        else:
            user = users.first()
        
        # Sample listings data
        sample_listings = [
            {
                'title': 'BMW 320d, 2018, stare excelentă',
                'description': 'Vând BMW 320d din 2018, cu 75.000 km parcurși. Mașina este în stare excelentă, service-ul la zi.',
                'price': 22500,
                'currency': 'EUR',
                'location': 'Cluj-Napoca',
                'category_name': 'Auto, Moto și Ambarcațiuni',
                'subcategory_name': 'Autoturisme',
            },
            {
                'title': 'Apartament 3 camere, Centrul Vechi',
                'description': 'Apartament modern cu 3 camere în centrul istoric al Bucureștiului. Renovat recent.',
                'price': 150000,
                'currency': 'EUR',
                'location': 'București, Sector 3',
                'category_name': 'Imobiliare',
                'subcategory_name': 'Apartamente de vânzare',
            },
            {
                'title': 'iPhone 14 Pro, 256GB, ca nou',
                'description': 'iPhone 14 Pro, 256GB, culoare Space Black. Folosit doar 6 luni, în stare impecabilă.',
                'price': 4500,
                'currency': 'RON',
                'location': 'Timișoara',
                'category_name': 'Electronice și Electrocasnice',
                'subcategory_name': 'Telefoane',
            },
            {
                'title': 'Dezvoltator Software - Remote',
                'description': 'Căutăm dezvoltator software cu experiență în Python și Django pentru echipa noastră.',
                'price': 8000,
                'currency': 'RON',
                'location': 'Remote',
                'category_name': 'Locuri de Muncă',
                'subcategory_name': 'Oferte de angajare',
            },
            {
                'title': 'Jachetă de piele, mărimea M',
                'description': 'Jachetă de piele originală, mărimea M, culoare neagră. Purtată de câteva ori.',
                'price': 800,
                'currency': 'RON',
                'location': 'Brașov',
                'category_name': 'Modă și Frumusețe',
                'subcategory_name': 'Haine bărbați',
            },
            {
                'title': 'Set mobilier living modern',
                'description': 'Set complet mobilier living: canapea, fotolii, masă de cafea. Design modern.',
                'price': 3500,
                'currency': 'RON',
                'location': 'Constanța',
                'category_name': 'Casă și Grădină',
                'subcategory_name': 'Mobilă/Decorațiuni',
            },
            {
                'title': 'Căruciorul copii 3 în 1',
                'description': 'Căruciorul pentru copii 3 în 1, include landou, scaun auto și căruciorul sport.',
                'price': 1200,
                'currency': 'RON',
                'location': 'Iași',
                'category_name': 'Mama și Copilul',
                'subcategory_name': 'Cărucioare/Scaune auto',
            },
            {
                'title': 'Bicicletă montană Trek, mărimea L',
                'description': 'Bicicletă montană Trek Marlin 7, mărimea L, roți 29", frâne hidraulice.',
                'price': 2800,
                'currency': 'RON',
                'location': 'Cluj-Napoca',
                'category_name': 'Sport, Timp Liber, Artă',
                'subcategory_name': 'Biciclete',
            },
            {
                'title': 'Cățel Labrador Retriever',
                'description': 'Cățel Labrador Retriever, 3 luni, vaccinat și deparazitat. Cu pedigree.',
                'price': 1500,
                'currency': 'RON',
                'location': 'București',
                'category_name': 'Animale de Companie',
                'subcategory_name': 'Câini',
            },
            {
                'title': 'Servicii de curățenie profesională',
                'description': 'Oferim servicii de curățenie profesională pentru case și apartamente în București.',
                'price': 150,
                'currency': 'RON',
                'location': 'București',
                'category_name': 'Servicii',
                'subcategory_name': 'Servicii pentru casă',
            },
        ]
        
        created_listings = 0
        for listing_data in sample_listings:
            try:
                # Find category and subcategory
                category = Category.objects.get(name=listing_data['category_name'])
                subcategory = Category.objects.get(
                    name=listing_data['subcategory_name'],
                    parent=category
                )
                
                listing = Listing.objects.create(
                    title=listing_data['title'],
                    description=listing_data['description'],
                    price=listing_data['price'],
                    currency=listing_data['currency'],
                    location=listing_data['location'],
                    user=user,
                    category=category,
                    subcategory=subcategory,
                    status='active'
                )
                created_listings += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f'Created listing: {listing.title}')
                )
                
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f'Category or subcategory not found for listing: {listing_data["title"]}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nCreated {created_listings} sample listings!')
        )
