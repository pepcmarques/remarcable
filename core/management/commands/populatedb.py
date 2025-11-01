from django.core.management.base import BaseCommand

from core.models import Category, Tag, Product

import json

data = json.load(open('core/management/commands/data.json'))

class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **options):
        print("Populating database...")
        for category_data in data['categories']:
            category, created = Category.objects.get_or_create(
                name=category_data['name']
            )
            if created:
                print(f"Created category: {category.name}")
            else:
                print(f"Category already exists: {category.name}")
        for tag_data in data['tags']:
            tag, created = Tag.objects.get_or_create(
                name=tag_data['name']
            )
            if created:
                print(f"Created tag: {tag.name}")
            else:
                print(f"Tag already exists: {tag.name}")
        for product_data in data['products']:
            category = Category.objects.get(name=product_data['category_name'])
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                category=category,
                price=product_data['price'],
                stock_count=product_data['stock_count'],
                description=product_data['description']
            )
            if created:
                print(f"Created product: {product.name}")
            else:
                print(f"Product already exists: {product.name}")
            for tag_name in product_data['tags']:
                tag = Tag.objects.get(name=tag_name)
                product.tags.add(tag)
        print("Database population complete.")