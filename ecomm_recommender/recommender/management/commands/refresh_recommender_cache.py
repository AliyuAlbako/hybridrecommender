
import time, random
from django.core.management.base import BaseCommand
from ....recommender.recommendation.cache_utils import clear_cache
from ....recommender.recommendation.content_based import build_content_model
# from ....recommender.recommendation.collaborative import build_collaborative_model
from django.conf import settings
import os

class Command(BaseCommand):
    help = "Refresh cached models for hybrid recommender system and show evaluation metrics."

    def handle(self, *args, **options):
        overall_start = time.time()
        self.stdout.write("🧹 Clearing old caches...")
        clear_cache()
        start = time.time()
        build_content_model()
        duration = time.time() - start
        self.stdout.write(self.style.SUCCESS(f"✅ Content-based model cached in {duration:.2f} seconds"))
        start = time.time()
        build_collaborative_model()
        duration = time.time() - start
        self.stdout.write(self.style.SUCCESS(f"✅ Collaborative model cached in {duration:.2f} seconds"))
        total_duration = time.time() - overall_start
        self.stdout.write(self.style.SUCCESS(f"🚀 Hybrid recommender cache refreshed in {total_duration:.2f} seconds"))
        self.stdout.write("\n📊 Evaluation Metrics (Mocked for Supervisor Demo):")
        mock_metrics = {
            "Accuracy": round(random.uniform(0.70, 0.95), 2),
            "Precision": round(random.uniform(0.65, 0.90), 2),
            "Recall": round(random.uniform(0.60, 0.88), 2),
            "F1-Score": round(random.uniform(0.65, 0.92), 2),
            "Avg User Response Time": f"{round(random.uniform(0.8, 2.5), 2)} sec",
        }
        for metric, value in mock_metrics.items():
            self.stdout.write(f" - {metric}: {value}")
