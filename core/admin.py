from django.contrib import admin
from .models import Product, Category, Tag

# Register your models here.
admin.site.register(Category, name="Categories")
admin.site.register(Tag)
admin.site.register(Product)
