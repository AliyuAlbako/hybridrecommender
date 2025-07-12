from django.core.management.base import BaseCommand
from recommender.models import Product
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seed the database with fake product data.'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of products to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        fake = Faker()

        categories = ['Electronics', 'Computers', 'Fashion', 'Home', 'Books', 'Beauty', 'Toys']
        sources = ['Internal', 'External', 'Affiliate']

        for _ in range(total):
            Product.objects.create(
                name=fake.unique.word().capitalize() + " " + fake.word().capitalize(),
                category=random.choice(categories),
                description=fake.paragraph(nb_sentences=5),
                price=round(random.uniform(10.00, 2000.00), 2),
                image_url=fake.image_url(),
                source=random.choice(sources),
                product_url=fake.url()
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully added {total} fake products.'))
