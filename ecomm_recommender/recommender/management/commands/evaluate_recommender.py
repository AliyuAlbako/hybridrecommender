from django.core.management.base import BaseCommand
from recommender.evaluate import run_all_evaluations
import json

class Command(BaseCommand):
    help = "Evaluate the hybrid recommendation system using ML and system-level metrics."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Running recommendation system evaluation..."))

        results = run_all_evaluations()

        # Print nicely formatted results
        self.stdout.write(json.dumps(results, indent=2))

        self.stdout.write(self.style.SUCCESS("✅ Evaluation complete!"))
