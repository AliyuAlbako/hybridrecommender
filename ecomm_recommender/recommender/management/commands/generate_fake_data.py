import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Product, UserInteraction, Rating

class Command(BaseCommand):
    help = "Generate synthetic users, ratings, and interactions for testing the recommender"

    def handle(self, *args, **options):
        self.stdout.write("Generating fake users, ratings, and interactions...")

        # Create users if not exist
        for i in range(1, 101):
            username = f"user{i}"
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, password="test1234")

        users = User.objects.all()
        products = list(Product.objects.all())

        if not products:
            self.stdout.write(self.style.ERROR("⚠️ No products in DB! Please add products first."))
            return

        for user in users:
            for _ in range(30):  # 30 random interactions
                product = random.choice(products)

                # Interaction
                UserInteraction.objects.create(
                    user=user,
                    product=product,
                    interaction_type=random.choice(["view", "like", "buy"]),
                    value=random.uniform(0.5, 1.5),
                )

                # Rating (1–5 scale)
                Rating.objects.update_or_create(
                    user=user,
                    product=product,
                    defaults={"rating": random.randint(1, 5)},
                )

        self.stdout.write(self.style.SUCCESS("✅ Fake data generated successfully!"))
