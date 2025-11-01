from django.db.models import Q
from .models import Product

def search_products(data):
    """
    Search and filter products based on given criteria.
    Works with both form.cleaned_data and serializer.validated_data
    """
    search_term = data.get('search', '')
    category = data.get('category')
    tags = data.get('tags', [])

    queryset = Product.objects.all()
    
    # Filter by search term
    if search_term:
        queryset = queryset.filter(
            Q(name__icontains=search_term) | Q(description__icontains=search_term)
        )
    
    # Filter by category
    if category:
        # In the case category is an object (from form)
        if hasattr(category, 'id'):
            queryset = queryset.filter(category_id=category.id)
        # In the case category is a string (from API)
        else:
            queryset = queryset.filter(category__name=category)
    
    # Filter by tags
    if tags:
        # In the case tags are objects (from form)
        if hasattr(tags[0], 'id'):
            tag_ids = [tag.id for tag in tags]
            queryset = queryset.filter(tags__id__in=tag_ids).distinct()
        # In the case tags are strings (from API)
        else:
            queryset = queryset.filter(tags__name__in=tags).distinct()
    
    return queryset.order_by('name')


