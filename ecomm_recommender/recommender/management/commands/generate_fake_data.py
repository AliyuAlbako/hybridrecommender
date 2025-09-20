import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recommender.models import Product, UserInteraction, Rating

class Command(BaseCommand):
    help = "Generate synthetic users, products, and interactions for testing hybrid recommender"

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=100, help="Number of fake users to create")
        parser.add_argument("--interactions", type=int, default=20, help="Number of interactions per user")
        parser.add_argument("--products", type=int, default=50, help="Number of products to ensure in DB")

    def handle(self, *args, **options):
        num_users = options["users"]
        num_interactions = options["interactions"]
        num_products = options["products"]

        # Step 1: Create products if not enough
        if Product.objects.count() < num_products:
            for i in range(num_products - Product.objects.count()):
                Product.objects.create(
                    name=f"Sample Product {i+1}",
                    category=random.choice(["Electronics", "Books", "Clothing", "Shoes"]),
                    description=f"This is a sample description for product {i+1}.",
                    price=random.uniform(5.0, 200.0),
                    image_url="https://via.placeholder.com/150",
                    source="MockStore",
                    product_url="https://example.com/product"
                )
            self.stdout.write(self.style.SUCCESS(f"Added {num_products} products."))

        products = list(Product.objects.all())

        # Step 2: Create users
        for i in range(num_users):
            username = f"user{i+1}"
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password("password123")
                user.save()

            # Step 3: Add random interactions
            for _ in range(num_interactions):
                product = random.choice(products)
                interaction_type = random.choice(["view", "like", "buy"])
                value = {"view": 1.0, "like": 2.0, "buy": 3.0}[interaction_type]

                UserInteraction.objects.create(
                    user=user,
                    product=product,
                    interaction_type=interaction_type,
                    value=value
                )

                # Optional rating
                if interaction_type in ["like", "buy"]:
                    Rating.objects.update_or_create(
                        user=user,
                        product=product,
                        defaults={"rating": random.randint(3, 5)}
                    )

        self.stdout.write(self.style.SUCCESS(
            f"✅ Created {num_users} users, each with {num_interactions} interactions."
        ))
