# recommender/recommendation/hybrid.py
from collections import Counter
from ..models import Product
from .content_based import get_content_recommendations
from .collaborative import get_collab_recommendations

def get_hybrid_recommendations(product_id, top_n=10, alpha=0.6):
    """
    alpha: weight for content-based (0..1). Collaborative weight = (1-alpha).
    Returns list of Product objects in ranked order.
    """
    content_ids = get_content_recommendations(product_id, top_n=top_n*3) or []
    collab_ids = get_collab_recommendations(product_id, top_n=top_n*3) or []

    scores = Counter()
    # higher rank -> higher score via reciprocal ranking
    for rank, pid in enumerate(content_ids):
        scores[pid] += alpha * (1.0 / (rank + 1))
    for rank, pid in enumerate(collab_ids):
        scores[pid] += (1 - alpha) * (1.0 / (rank + 1))

    # remove the original product
    if product_id in scores:
        del scores[product_id]

    ranked = [pid for pid, _ in scores.most_common(top_n)]
    # fetch products preserving order
    products = list(Product.objects.filter(id__in=ranked))
    products_sorted = sorted(products, key=lambda p: ranked.index(p.id) if p.id in ranked else len(ranked))
    return products_sorted
