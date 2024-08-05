from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from catalog.models import Attribute, Category, ProductType, Product, ProductVariation, ProductImage, ProductAttribute
from faker import Faker
import random
from django.utils.text import slugify
from django.core.files import File

fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Create Attributes
        attribute_types = [
            {'name': 'Color', 'data_type': 'choice', 'choices': {'choices': ['Red', 'Blue', 'Green', 'Black', 'White']}},
            {'name': 'Size', 'data_type': 'choice', 'choices': {'choices': ['Small', 'Medium', 'Large', 'Extra Large']}},
            {'name': 'Weight', 'data_type': 'float', 'choices': None},
            {'name': 'Available', 'data_type': 'boolean', 'choices': None},
            {'name': 'Manufacture Date', 'data_type': 'date', 'choices': None},
        ]
        for attr in attribute_types:
            defaults = {
                'data_type': attr['data_type'],
                'choices': attr.get('choices')
            }
            Attribute.objects.update_or_create(name=attr['name'], defaults=defaults)

        # Create ProductTypes first
        product_types = [
            {'name': 'Gadget', 'description': 'Electronic gadgets and devices', 'attributes': ['Color', 'Weight']},
            {'name': 'Apparel', 'description': 'Clothing and accessories', 'attributes': ['Size', 'Available']},
            {'name': 'Furniture', 'description': 'Furniture for home and office', 'attributes': ['Weight']},
            {'name': 'Books', 'description': 'Various genres of books', 'attributes': ['Manufacture Date']},
        ]
        for ptype in product_types:
            attributes = Attribute.objects.filter(name__in=ptype['attributes'])
            product_type, created = ProductType.objects.update_or_create(
                name=ptype['name'],
                defaults={'description': ptype['description']}
            )
            product_type.attributes.set(attributes)
            product_type.save()

        top_level_categories = [
            {'name': 'Electronics', 'slug': slugify('Electronics'), 'description': fake.text(), 'parent': None,
             'product_type': ProductType.objects.get(name='Gadget')},
            {'name': 'Clothing', 'slug': slugify('Clothing'), 'description': fake.text(), 'parent': None,
             'product_type': ProductType.objects.get(name='Apparel')},
            {'name': 'Furniture', 'slug': slugify('Furniture'), 'description': fake.text(), 'parent': None,
             'product_type': ProductType.objects.get(name='Furniture')},
            {'name': 'Home Appliances', 'slug': slugify('Home Appliances'), 'description': fake.text(), 'parent': None,
             'product_type': ProductType.objects.get(name='Gadget')},
            {'name': 'Books', 'slug': slugify('Books'), 'description': fake.text(), 'parent': None,
             'product_type': ProductType.objects.get(name='Books')},
        ]

        for cat in top_level_categories:
            Category.objects.update_or_create(name=cat['name'], defaults=cat)

        # Retrieve created top-level categories for reference
        electronics = Category.objects.get(name='Electronics')
        clothing = Category.objects.get(name='Clothing')
        furniture = Category.objects.get(name='Furniture')
        home_appliances = Category.objects.get(name='Home Appliances')
        books = Category.objects.get(name='Books')

        sub_categories = [
            {'name': 'Smartphones', 'slug': slugify('Smartphones'), 'description': fake.text(),
             'parent': electronics, 'product_type': ProductType.objects.get(name='Gadget')},
            {'name': 'Laptops', 'slug': slugify('Laptops'), 'description': fake.text(),
             'parent': electronics, 'product_type': ProductType.objects.get(name='Gadget')},
            {'name': 'Men', 'slug': slugify('Men'), 'description': fake.text(),
             'parent': clothing, 'product_type': ProductType.objects.get(name='Apparel')},
            {'name': 'Women', 'slug': slugify('Women'), 'description': fake.text(),
             'parent': clothing, 'product_type': ProductType.objects.get(name='Apparel')},
            {'name': 'Office Furniture', 'slug': slugify('Office Furniture'), 'description': fake.text(),
             'parent': furniture, 'product_type': ProductType.objects.get(name='Furniture')},
            {'name': 'Living Room Furniture', 'slug': slugify('Living Room Furniture'), 'description': fake.text(),
             'parent': furniture, 'product_type': ProductType.objects.get(name='Furniture')},
            {'name': 'Refrigerators', 'slug': slugify('Refrigerators'), 'description': fake.text(),
             'parent': home_appliances, 'product_type': ProductType.objects.get(name='Gadget')},
            {'name': 'Washing Machines', 'slug': slugify('Washing Machines'), 'description': fake.text(),
             'parent': home_appliances, 'product_type': ProductType.objects.get(name='Gadget')},
            {'name': 'Fiction', 'slug': slugify('Fiction'), 'description': fake.text(),
             'parent': books, 'product_type': ProductType.objects.get(name='Books')},
            {'name': 'Non-Fiction', 'slug': slugify('Non-Fiction'), 'description': fake.text(),
             'parent': books, 'product_type': ProductType.objects.get(name='Books')},
        ]

        for cat in sub_categories:
            Category.objects.update_or_create(name=cat['name'], defaults=cat)

        # Create Products
        num_products = 100  # Set the number of products you want to create
        category_objects = list(Category.objects.all())  # Convert QuerySet to list
        product_objects = []
        for _ in range(num_products):
            product = {
                'name': fake.word() + " " + fake.word(),
                'description': fake.text(),
                'product_type': random.choice(ProductType.objects.all()),
                'categories': random.sample(category_objects, k=random.randint(1, 3)),
                'sku': fake.unique.ean13(),
                'price': round(random.uniform(10, 1000), 2),
                'stock_quantity': random.randint(1, 500),
                'weight': round(random.uniform(0.1, 50.0), 2),
                'length': round(random.uniform(1.0, 200.0), 2),
                'width': round(random.uniform(1.0, 200.0), 2),
                'height': round(random.uniform(1.0, 200.0), 2)
            }
            categories = product.pop('categories')
            prod = Product.objects.create(**product)
            prod.categories.set(categories)
            product_objects.append(prod)

        # Create ProductVariations
        for product in product_objects:
            num_variations = random.randint(1, 5)  # Number of variations per product
            for _ in range(num_variations):
                variation = {
                    'product': product,
                    'name': fake.word(),
                    'price': round(random.uniform(10, 1000), 2),
                    'stock': random.randint(1, 100),
                    'attributes': {
                        'Color': random.choice(['Red', 'Blue', 'Green', 'Black', 'White']),
                        'Size': random.choice(['Small', 'Medium', 'Large', 'Extra Large']),
                        'Weight': round(random.uniform(0.1, 50.0), 2),
                        'Available': random.choice([True, False]),
                        'Manufacture Date': str(fake.date_this_decade())
                    }
                }
                ProductVariation.objects.create(**variation)

        # Create ProductImages for Products
        image_paths = {
            'Smartphone XYZ': 'seed_images/1.jpg',
            'Leather Jacket': 'seed_images/2.jpg',
            'Office Desk': 'seed_images/1.jpg',
            'Fantasy Novel': 'seed_images/2.jpg',
        }

        for product in product_objects:
            image_path = image_paths.get(product.name, 'seed_images/1.jpg')
            with open(image_path, 'rb') as image_file:
                ProductImage.objects.create(
                    product=product,
                    image=File(image_file),
                    alt_text=f'{product.name} image',
                    is_thumbnail=True,
                    is_primary=True
                )

        # Create ProductImages for Variations
        variation_image_paths = {
            'Midnight Black': 'seed_images/1.jpg',
            'Classic White': 'seed_images/2.jpg',
            'Size M': 'seed_images/2.jpg',
            'Wood Finish': 'seed_images/1.jpg',
            'Paperback': 'seed_images/1.jpg',
        }

        for variation in ProductVariation.objects.all():
            image_path = variation_image_paths.get(variation.name, 'seed_images/2.jpg')
            with open(image_path, 'rb') as image_file:
                ProductImage.objects.create(
                    product=variation.product,
                    image=File(image_file),
                    alt_text=f'{variation.name} image',
                    is_thumbnail=False,
                    is_primary=False
                )

        # Create ProductAttributes
        for product in product_objects:
            attributes = [
                {'product': product, 'attribute_type': random.choice(Attribute.objects.all()), 'value': fake.word()},
                {'product': product, 'attribute_type': random.choice(Attribute.objects.all()),
                 'value': round(random.uniform(0.1, 50.0), 2)},
                {'product': product, 'attribute_type': random.choice(Attribute.objects.all()),
                 'value': str(fake.date_this_decade())},
                {'product': product, 'attribute_type': random.choice(Attribute.objects.all()), 'value': fake.boolean()},
                # Add more attributes with different data types
            ]
            [ProductAttribute.objects.create(**attr) for attr in attributes]
        self.stdout.write(self.style.SUCCESS('Database seeding completed.'))

        # Create a user
        username = 'testUser'
        password = 'testUser'
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created user {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))
