from django.core.cache import cache
from typing import List, Dict, Any, Optional
from .models import Listing, Category

class ListingService:
    @classmethod
    def get_featured_listings(cls) -> List[Dict[str, Any]]:
        """Get featured listings with caching"""
        cache_key = 'featured_listings'
        listings = cache.get(cache_key)
        if not listings:
            listings = list(Listing.objects.filter(
                is_featured=True,
                status='active'
            ).select_related('category', 'user').values(
                'id', 'title', 'price', 'currency',
                'location', 'category__name', 'user__username'
            ))
            cache.set(cache_key, listings, timeout=3600)  # Cache for 1 hour
        return listings

    @classmethod
    def get_marketplace_context(cls) -> Dict[str, Any]:
        """Get complete marketplace context"""
        from django.db.models import Count
        from datetime import datetime
        
        # Get categories with hierarchical structure
        main_categories = list(Category.objects.filter(
            parent__isnull=True
        ).values('id', 'name', 'slug', 'icon', 'color'))
        
        # Get subcategories grouped by parent
        subcategories = {}
        for subcat in Category.objects.filter(parent__isnull=False).values(
            'id', 'name', 'slug', 'parent_id', 'icon', 'color'
        ):
            parent_id = subcat['parent_id']
            if parent_id not in subcategories:
                subcategories[parent_id] = []
            subcategories[parent_id].append(subcat)
        
        # Build complete category structure
        categories_structure = []
        for category in main_categories:
            cat_data = dict(category)
            cat_data['subcategories'] = subcategories.get(category['id'], [])
            categories_structure.append(cat_data)
        
        # Get recent listings
        recent_listings = list(Listing.objects.filter(
            status='active'
        ).select_related('category', 'user').values(
            'id', 'title', 'price', 'currency',
            'location', 'category__name', 'created_at'
        ).order_by('-created_at')[:20])
        
        return {
            'categories': main_categories,
            'categories_structure': categories_structure,
            'recent_listings': recent_listings,
            'last_updated': datetime.now().isoformat()
        }

    @classmethod
    def get_category_context(cls, category_slug: str, page: Optional[str] = None) -> Dict[str, Any]:
        """Get context for category detail page"""
        from django.core.paginator import Paginator
        from django.db.models import Count
        from datetime import datetime
        
        # Get category and its subcategories
        category = Category.objects.filter(slug=category_slug).first()
        if not category:
            return {
                'category': None,
                'subcategories': [],
                'listings': [],
                'last_updated': datetime.now().isoformat()
            }
            
        subcategories = list(Category.objects.filter(parent=category).all())
        
        # Get listings for this category and subcategories
        category_ids = [category.pk] + [sc.pk for sc in subcategories]
        listings = Listing.objects.filter(
            category__pk__in=category_ids,
            status='active'
        ).select_related('category', 'user')
        
        # Paginate listings
        paginator = Paginator(listings, 20)
        page_obj = paginator.get_page(page)
        
        return {
            'category': {
                'pk': category.pk,
                'name': category.name,
                'slug': category.slug,
                'description': getattr(category, 'description', ''),
                'icon': category.icon,
                'color': category.color
            },
            'subcategories': [{
                'pk': sc.pk,
                'name': sc.name,
                'slug': sc.slug,
                'icon': sc.icon,
                'color': sc.color
            } for sc in subcategories],
            'listings': page_obj,
            'last_updated': datetime.now().isoformat()
        }

class CategoryService:
    @classmethod
    def get_category_tree(cls) -> List[Dict[str, Any]]:
        """Get complete category hierarchy"""
        cache_key = 'category_tree'
        tree = cache.get(cache_key)
        if not tree:
            tree = cls._build_category_tree()
            cache.set(cache_key, tree, timeout=86400)  # Cache for 24 hours
        return tree
    
    @classmethod
    def _build_category_tree(cls) -> List[Dict[str, Any]]:
        """Build category tree structure"""
        main_categories = Category.objects.filter(parent__isnull=True)
        tree = []
        
        for category in main_categories:
            category_data = {
                'id': category.pk,  # Use pk instead of id
                'name': category.name,
                'slug': category.slug,
                'subcategories': []
            }
            
            subcategories = Category.objects.filter(parent=category)
            for subcat in subcategories:
                category_data['subcategories'].append({
                    'id': subcat.pk,  # Use pk instead of id
                    'name': subcat.name,
                    'slug': subcat.slug
                })
            
            tree.append(category_data)
        
        return tree