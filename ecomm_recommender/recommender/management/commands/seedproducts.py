import json
import os
from django.core.management.base import BaseCommand
from recommender.models import Product

class Command(BaseCommand):
    help = "Seed the database with products from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to the JSON file containing products'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        if not file_path:
            self.stdout.write(self.style.ERROR("Please provide a JSON file path using --file"))
            return

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            products = json.load(f)

        created_count = 0
        for prod in products:
            Product.objects.get_or_create(
                name=prod.get("name", ""),
                description=prod.get("description", ""),
                price=prod.get("price", 0.0),
                image_url=prod.get("image_url", ""),
                source=prod.get("source", "Unknown"),
                category=prod.get("category", "General")
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created_count} products from {file_path}"))
