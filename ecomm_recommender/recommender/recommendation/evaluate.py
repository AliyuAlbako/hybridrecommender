# recommender/recommendation/evaluate.py
import random
import numpy as np
from collections import defaultdict
from .cache_utils import clear_cache
from .content_based import build_content_model, get_content_recommendations
from .collaborative import build_collab_model, get_collab_recommendations
from .hybrid import get_hybrid_recommendations
from ..models import UserInteraction, Product
from django.db.models import Count

def train_test_split_interactions(test_fraction=0.2, seed=42):
    qs = UserInteraction.objects.all().values("id", "user_id", "product_id", "value")
    interactions = list(qs)
    random.Random(seed).shuffle(interactions)
    n_test = int(len(interactions) * test_fraction)
    test = interactions[:n_test]
    train = interactions[n_test:]
    return train, test

def evaluate_topk_for_item_recs(k=5, alpha=0.6):
    """
    Evaluate hybrid recommender for item-to-item recommendations.
    We hide a fraction of interactions (test), rebuild models on train,
    and check whether held-out products for users are recommended when querying
    the product they interacted with in test.
    """
    # create train/test
    train, test = train_test_split_interactions(test_fraction=0.2)
    if not train:
        print("Not enough interactions for evaluation.")
        return {}

    # Build models on train by temporarily writing train into a temp table approach
    # Simpler approach here: clear cache, build models using current DB (assumes you can set UserInteraction to train)
    # For robust eval you should create temp DB or fixtures. Here we will:
    # 1) Clear cache
    clear_cache()
    # 2) Build models (these will use DB — ensure DB is train-only if you temporarily modify it)
    build_content_model()
    build_collab_model()

    # Map user -> held_out products from test
    user_heldout = defaultdict(set)
    for r in test:
        user_heldout[r["user_id"]].add(r["product_id"])

    precision_list = []
    recall_list = []
    for user_id, heldout_products in user_heldout.items():
        # for each held out product, try to see if any recommended from a seed product
        hits = 0
        total_relevant = len(heldout_products)
        total_recommended = 0
        for target_pid in heldout_products:
            recs = get_hybrid_recommendations(target_pid, top_n=k, alpha=alpha)
            rec_ids = [p.id for p in recs]
            total_recommended += len(rec_ids)
            hits += len(set(rec_ids) & heldout_products)
        if total_recommended == 0:
            continue
        precision = hits / total_recommended
        recall = hits / total_relevant
        precision_list.append(precision)
        recall_list.append(recall)

    results = {
        "Precision@{}".format(k): round(np.mean(precision_list), 4) if precision_list else 0.0,
        "Recall@{}".format(k): round(np.mean(recall_list), 4) if recall_list else 0.0,
    }
    return results
