from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower


class CategoryManager(models.Manager):
    """
    Custom manager for the Category model.
    """
    
    def get_by_name(self, name):
        """
        Returns a single Category object matching the name (case-insensitive).
        """
        return self.get_queryset().get(name__iexact=name)
        
    def with_product_count(self):
        """
        Annotates the queryset with the number of products in each category.
        """
        return self.get_queryset().annotate(
            product_count=models.Count('products')
        ).order_by('-product_count')


class Category(models.Model):
    """
    Category model.
    """
    name = models.CharField(max_length=100, null=False, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"

        constraints = [
            models.UniqueConstraint(
                Lower('name'), 
                name='name_unique_ci'
            )
        ]

    #objects = CategoryManager()

    def __str__(self):
        return self.name


class TagManager(models.Manager):
    """
    Custom manager for the Tag model.
    """
    
    def get_with_product_list(self, tag_name):
        """
        Returns a single Tag object along with a list of its products.
        """
        return self.get_queryset().prefetch_related('products').get(tag_name__iexact=tag_name)
        
    def with_product_count(self):
        """
        Annotates the queryset with the number of products associated with each tag.
        """
        return self.get_queryset().annotate(
            product_count=models.Count('products')
        ).order_by('-product_count')


class Tag(models.Model):
    tag_name = models.CharField(max_length=50, null=False)

    #objects = TagManager()

    def __str__(self):
        return self.tag_name


class ProductManager(models.Manager):
    """
    Custom manager for the Product model, specializing in search and filtering.
    """

    def filter_and_search(self, search_term=None, category_id=None, tag_ids=None):
        """
        Combines search by product name/description with filtering by category and tags.
        """
        queryset = self.get_queryset()

        # Search (by product name or description - Assignment requested description)
        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term) |
                Q(description__icontains=search_term)
            )

        # Filter by Category
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Filter by Tags
        if tag_ids:
            queryset = queryset.filter(tags__in=tag_ids).distinct()

        return queryset.select_related('category').prefetch_related('tags')

    def in_stock(self):
        """
        Filter to ensure products are available in stock.
        """
        return self.get_queryset().filter(stock_count__gt=0)


class Product(models.Model):
    """
    Product model.
    """
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)
    stock_count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'), 
                name='name_unique_case_insensitive'
            ),
            models.CheckConstraint(
                check=models.Q(stock_count__gt=0),
                name='stock_count_must_be_gt0'
            ),
            models.CheckConstraint(
                check=models.Q(price__gt=0),
                name='price_must_be_gt0'
            ),
        ]

    objects = ProductManager()

    def __str__(self):
        return self.name
