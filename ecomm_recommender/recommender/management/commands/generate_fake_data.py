# recommender/management/commands/generate_fake_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Product, UserInteraction, Rating, UserProfile
import random

class Command(BaseCommand):
    help = "Generate fake users, profiles, interactions, and ratings (without touching real products)."

    def handle(self, *args, **kwargs):
        # Sample hobbies & interests
        hobbies = ["Reading", "Sports", "Gaming", "Travel", "Music", "Art"]
        interests = ["Tech", "Fashion", "Electronics", "Books", "Home Decor", "Health"]

        # 🧹 Clear only user-related data
        User.objects.exclude(is_superuser=True).delete()
        UserProfile.objects.all().delete()
        UserInteraction.objects.all().delete()
        Rating.objects.all().delete()

        # Get existing products (scraped ones)
        products = list(Product.objects.all())
        if not products:
            self.stdout.write(self.style.WARNING("⚠️ No products found — please run scrape_real_products first."))
            return

        # 👤 Create users + profiles
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

        # 💬 Create interactions and ratings
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

        self.stdout.write(self.style.SUCCESS("✅ Users, profiles, interactions, and ratings generated successfully!"))
