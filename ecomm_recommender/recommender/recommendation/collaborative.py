# recommender/recommendation/collaborative.py
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from ..models import UserInteraction
from .cache_utils import load_cache, save_cache

CACHE_NAME = "collab_model.pkl"

def build_collab_model(min_interactions_per_user=1):
    # interactions: user_id, product_id, value
    qs = UserInteraction.objects.all().values("user_id", "product_id", "value")
    df = pd.DataFrame(list(qs))
    if df.empty:
        model = {"prod_ids": [], "sim": None, "pivot_index": None}
        save_cache(model, CACHE_NAME)
        return model

    # Pivot: users x products
    pivot = df.pivot_table(index="user_id", columns="product_id", values="value", aggfunc="sum", fill_value=0)
    if pivot.shape[1] < 2:
        model = {"prod_ids": list(pivot.columns), "sim": None, "pivot_index": pivot.index}
        save_cache(model, CACHE_NAME)
        return model

    item_matrix = pivot.T  # products x users
    sim = cosine_similarity(item_matrix)  # item-item
    prod_ids = list(item_matrix.index)

    model = {"prod_ids": prod_ids, "sim": sim, "pivot_index": pivot.index}
    save_cache(model, CACHE_NAME)
    return model

def get_collab_model():
    model = load_cache(CACHE_NAME)
    if model is None:
        model = build_collab_model()
    return model

def get_collab_recommendations(product_id, top_n=10):
    model = get_collab_model()
    prod_ids = model.get("prod_ids", [])
    sim = model.get("sim", None)
    if not prod_ids or sim is None:
        return []
    if product_id not in prod_ids:
        return []
    idx = prod_ids.index(product_id)
    sim_scores = list(enumerate(sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1: top_n + 1]
    recommended_ids = [prod_ids[i] for i, _ in sim_scores]
    return recommended_ids
