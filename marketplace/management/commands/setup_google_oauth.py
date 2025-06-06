from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
import os

class Command(BaseCommand):
    help = 'Setup Google OAuth for Piata.ro'

    def add_arguments(self, parser):
        parser.add_argument(
            '--client-id',
            type=str,
            help='Google OAuth Client ID'
        )
        parser.add_argument(
            '--client-secret',
            type=str,
            help='Google OAuth Client Secret'
        )
        parser.add_argument(
            '--site-domain',
            type=str,
            default='localhost:8000',
            help='Site domain (default: localhost:8000)'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Setting up Google OAuth for Piata.ro...')
        )

        # Update site domain
        site_domain = options['site_domain']
        site, created = Site.objects.get_or_create(
            pk=1,
            defaults={'domain': site_domain, 'name': 'Piata.ro'}
        )
        if not created:
            site.domain = site_domain
            site.name = 'Piata.ro'
            site.save()
        
        self.stdout.write(f'✅ Site configured: {site.domain}')

        # Get credentials from arguments or environment
        client_id = options['client_id'] or os.getenv('GOOGLE_CLIENT_ID')
        client_secret = options['client_secret'] or os.getenv('GOOGLE_CLIENT_SECRET')

        if not client_id or not client_secret:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  Google OAuth credentials not provided.\n'
                    'You can:\n'
                    '1. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables\n'
                    '2. Use --client-id and --client-secret arguments\n'
                    '3. Configure manually in Django admin at /admin/socialaccount/socialapp/'
                )
            )
            return

        # Create or update Social Application
        social_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google',
                'client_id': client_id,
                'secret': client_secret,
            }
        )

        if not created:
            social_app.client_id = client_id
            social_app.secret = client_secret
            social_app.save()

        # Associate with site
        social_app.sites.clear()
        social_app.sites.add(site)

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Google OAuth configured successfully!\n'
                f'   Client ID: {client_id[:20]}...\n'
                f'   Associated with site: {site.domain}\n\n'
                f'🌐 Test your setup:\n'
                f'   1. Start server: python manage.py runserver\n'
                f'   2. Visit: http://localhost:8000/accounts/login/\n'
                f'   3. Click "Continue with Google"\n'
            )
        )
