from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower


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

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Tag model.
    """
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    """
    Custom manager for the Product model, used for search and filtering.
    """

    def filter_and_search(self, search_term=None, category_id=None, tag_ids=None):
        """
        Combines search by product name/description with filtering by category and tags.
        """
        queryset = self.get_queryset()

        # Search (by product name or description)
        if search_term:
            # NOTE: Explained in README why I would use embeddings.
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


class Product(models.Model):
    """
    Product model.
    """

    # Although the assignment requested only the description field, 
    # I am adding more fields to make the model more realistic, and creating some constraints.
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
