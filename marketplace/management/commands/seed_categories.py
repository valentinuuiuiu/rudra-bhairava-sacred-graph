from django.core.management.base import BaseCommand
from marketplace.models import Category


class Command(BaseCommand):
    help = 'Seed the database with comprehensive categories and subcategories'

    def handle(self, *args, **options):
        categories_data = [
            {
                'name': 'Cars',
                'slug': 'cars',
                'icon': 'fas fa-car',
                'color': '#3B82F6',
                'subcategories': [
                    {'name': 'Used Cars', 'slug': 'used-cars', 'icon': 'fas fa-car'},
                    {'name': 'New Cars', 'slug': 'new-cars', 'icon': 'fas fa-car-side'},
                    {'name': 'Motorcycles', 'slug': 'motorcycles', 'icon': 'fas fa-motorcycle'},
                    {'name': 'Trucks', 'slug': 'trucks', 'icon': 'fas fa-truck'},
                    {'name': 'Car Parts', 'slug': 'car-parts', 'icon': 'fas fa-cog'},
                ]
            },
            {
                'name': 'Electronics',
                'slug': 'electronics',
                'icon': 'fas fa-laptop',
                'color': '#10B981',
                'subcategories': [
                    {'name': 'Mobile Phones', 'slug': 'mobile-phones', 'icon': 'fas fa-mobile-alt'},
                    {'name': 'Computers', 'slug': 'computers', 'icon': 'fas fa-desktop'},
                    {'name': 'Gaming', 'slug': 'gaming', 'icon': 'fas fa-gamepad'},
                    {'name': 'TV & Audio', 'slug': 'tv-audio', 'icon': 'fas fa-tv'},
                    {'name': 'Cameras', 'slug': 'cameras', 'icon': 'fas fa-camera'},
                ]
            },
            {
                'name': 'Real Estate',
                'slug': 'real-estate',
                'icon': 'fas fa-home',
                'color': '#8B5CF6',
                'subcategories': [
                    {'name': 'Apartments for Sale', 'slug': 'apartments-sale', 'icon': 'fas fa-building'},
                    {'name': 'Houses for Sale', 'slug': 'houses-sale', 'icon': 'fas fa-home'},
                    {'name': 'Apartments for Rent', 'slug': 'apartments-rent', 'icon': 'fas fa-key'},
                    {'name': 'Commercial', 'slug': 'commercial', 'icon': 'fas fa-store'},
                    {'name': 'Land', 'slug': 'land', 'icon': 'fas fa-map'},
                ]
            },
            {
                'name': 'Jobs',
                'slug': 'jobs',
                'icon': 'fas fa-briefcase',
                'color': '#F59E0B',
                'subcategories': [
                    {'name': 'IT & Technology', 'slug': 'it-technology', 'icon': 'fas fa-code'},
                    {'name': 'Sales & Marketing', 'slug': 'sales-marketing', 'icon': 'fas fa-chart-line'},
                    {'name': 'Healthcare', 'slug': 'healthcare', 'icon': 'fas fa-stethoscope'},
                    {'name': 'Education', 'slug': 'education', 'icon': 'fas fa-graduation-cap'},
                    {'name': 'Construction', 'slug': 'construction', 'icon': 'fas fa-hard-hat'},
                ]
            },
            {
                'name': 'Services',
                'slug': 'services',
                'icon': 'fas fa-tools',
                'color': '#EF4444',
                'subcategories': [
                    {'name': 'Home Services', 'slug': 'home-services', 'icon': 'fas fa-hammer'},
                    {'name': 'Beauty & Wellness', 'slug': 'beauty-wellness', 'icon': 'fas fa-spa'},
                    {'name': 'Tutoring', 'slug': 'tutoring', 'icon': 'fas fa-chalkboard-teacher'},
                    {'name': 'Pet Services', 'slug': 'pet-services', 'icon': 'fas fa-paw'},
                    {'name': 'Event Services', 'slug': 'event-services', 'icon': 'fas fa-calendar-check'},
                ]
            },
            {
                'name': 'Fashion & Style',
                'slug': 'fashion-style',
                'icon': 'fas fa-tshirt',
                'color': '#EC4899',
                'subcategories': [
                    {'name': 'Women\'s Clothing', 'slug': 'womens-clothing', 'icon': 'fas fa-female'},
                    {'name': 'Men\'s Clothing', 'slug': 'mens-clothing', 'icon': 'fas fa-male'},
                    {'name': 'Shoes', 'slug': 'shoes', 'icon': 'fas fa-shoe-prints'},
                    {'name': 'Accessories', 'slug': 'accessories', 'icon': 'fas fa-gem'},
                    {'name': 'Bags', 'slug': 'bags', 'icon': 'fas fa-shopping-bag'},
                ]
            },
            {
                'name': 'Sports & Hobbies',
                'slug': 'sports-hobbies',
                'icon': 'fas fa-dumbbell',
                'color': '#06B6D4',
                'subcategories': [
                    {'name': 'Fitness Equipment', 'slug': 'fitness-equipment', 'icon': 'fas fa-dumbbell'},
                    {'name': 'Sports Gear', 'slug': 'sports-gear', 'icon': 'fas fa-football-ball'},
                    {'name': 'Outdoor & Camping', 'slug': 'outdoor-camping', 'icon': 'fas fa-campground'},
                    {'name': 'Musical Instruments', 'slug': 'musical-instruments', 'icon': 'fas fa-music'},
                    {'name': 'Books & Media', 'slug': 'books-media', 'icon': 'fas fa-book'},
                ]
            }
        ]

        self.stdout.write('Starting category seeding...')

        for cat_data in categories_data:
            # Get or create main category
            main_cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'icon': cat_data['icon'],
                    'color': cat_data['color']
                }
            )

            if not created:
                # Update existing category with new data
                main_cat.icon = cat_data['icon']
                main_cat.color = cat_data['color']
                main_cat.save()

            action = "Created" if created else "Updated"
            self.stdout.write(f'{action} main category: {main_cat.name}')

            # Create subcategories
            for subcat_data in cat_data['subcategories']:
                subcat, sub_created = Category.objects.get_or_create(
                    slug=subcat_data['slug'],
                    defaults={
                        'name': subcat_data['name'],
                        'icon': subcat_data['icon'],
                        'parent': main_cat
                    }
                )

                if not sub_created:
                    # Update existing subcategory using update method
                    Category.objects.filter(pk=subcat.pk).update(
                        icon=subcat_data['icon'],
                        parent=main_cat
                    )

                action = "Created" if sub_created else "Updated"
                self.stdout.write(f'  {action} subcategory: {subcat.name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded categories!')
        )
