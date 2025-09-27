# recommender/management/commands/generate_fake_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Product, UserInteraction, Rating, UserProfile
import random

class Command(BaseCommand):
    help = "Generate fake products, users, ratings, interactions, and profiles with images"

    def handle(self, *args, **kwargs):
        # Sample categories with placeholder images
        category_images = {
            "Electronics": "https://picsum.photos/seed/electronics{}/400/400",
            "Fashion": "https://picsum.photos/seed/fashion{}/400/400",
            "Books": "https://picsum.photos/seed/books{}/400/400",
            "Sports": "https://picsum.photos/seed/sports{}/400/400",
            "Home": "https://picsum.photos/seed/home{}/400/400",
        }

        categories = list(category_images.keys())

        # Sample hobbies & interests
        hobbies = ["gaming", "reading", "cooking", "traveling", "fitness"]
        interests = ["electronics", "fashion", "books", "sports", "home decor"]

        # Clear existing
        Product.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        UserProfile.objects.all().delete()

        # Create users + profiles
        users = []
        for i in range(10):
            user = User.objects.create_user(
                username=f"user{i}",
                email=f"user{i}@test.com",
                password="password123"
            )
            profile = UserProfile.objects.create(
                user=user,
                hobby=random.choice(hobbies),
                interest=random.choice(interests)
            )
            users.append(user)

        # Create products with image URLs
        products = []
        for i in range(20):
            category = random.choice(categories)
            image_url = category_images[category].format(i)

            product = Product.objects.create(
                name=f"{category} Product {i}",
                category=category,
                description=f"This is a sample {category.lower()} product number {i}.",
                price=round(random.uniform(10, 500), 2),
                image_url=image_url,
                source="Internal",
                product_url=f"https://example.com/product/{i}"
            )
            products.append(product)

        # Add interactions + ratings
        for user in users:
            for _ in range(5):  # each user interacts with 5 random products
                product = random.choice(products)
                UserInteraction.objects.create(
                    user=user,
                    product=product,
                    interaction_type=random.choice(["view", "like", "buy"]),
                    value=random.uniform(0.5, 2.0)
                )
                Rating.objects.update_or_create(
                    user=user,
                    product=product,
                    defaults={"rating": random.randint(1, 5)}
                )

        self.stdout.write(self.style.SUCCESS("Fake data with profiles & images generated successfully!"))
