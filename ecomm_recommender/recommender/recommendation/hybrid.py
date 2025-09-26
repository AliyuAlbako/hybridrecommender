# recommender/recommendation/hybrid.py

from ..models import Product, UserProfile, UserInteraction
from django.db.models import Q
from .external_scraper import scrape_jumia, scrape_konga, scrape_amazon  # ✅ real Jumia scraper


def fetch_from_konga(category_or_keyword):
    """Try scraping Konga, fallback to mocked product if fails."""
    try:
        results = scrape_konga(category_or_keyword)
        if results and isinstance(results, list):
            return results
    except Exception as e:
        print("⚠️ Konga scrape failed:", e)

    # --- fallback ---
    return [
        {
            "platform": "Konga",
            "name": "Oraimo 27000mAh Power Bank",
            "price": "₦18,500",
            "url": "https://www.konga.com/product/oraimo-27000mah-power-bank",
            "image_url": "https://www.konga.com/product-image.jpg",
        }
    ]


def fetch_from_amazon(category_or_keyword):
    """Try scraping Amazon, fallback to mocked product if fails."""
    try:
        results = scrape_amazon(category_or_keyword)
        if results and isinstance(results, list):
            return results
    except Exception as e:
        print("⚠️ Amazon scrape failed:", e)

    # --- fallback ---
    return [
        {
            "platform": "Amazon",
            "name": "Anker 20,000mAh Portable Charger",
            "price": "$45",
            "url": "https://www.amazon.com/dp/B08XYZ123",
            "image_url": "https://m.media-amazon.com/images/I/71AnkerPowerBank.jpg",
        }
    ]


def get_hybrid_recommendations(user_id=None, product_id=None, top_n=10, alpha=0.6):
    """
    Hybrid recommendations:
    - Internal DB recommendations
    - Personalized by hobby/interest
    - External products from Jumia (real), Konga (mock), Amazon (mock)
    """

    products = Product.objects.all()

    # -----------------------
    # Internal recommendations
    # -----------------------
    if product_id:
        target = Product.objects.get(id=product_id)
        products = products.exclude(id=target.id)

        content_based = products.filter(
            Q(category__icontains=target.category) |
            Q(description__icontains=target.name)
        )
    else:
        target = None
        content_based = products

    collaborative_ids = []
    if product_id:
        interactions = UserInteraction.objects.filter(product_id=product_id)
        user_ids = interactions.values_list("user_id", flat=True)
        collaborative_ids = UserInteraction.objects.filter(
            user_id__in=user_ids
        ).values_list("product_id", flat=True)

    collaborative = products.filter(id__in=collaborative_ids)

    personal = []
    keyword = None
    if user_id:
        try:
            profile = UserProfile.objects.get(user_id=user_id)
            hobby = profile.hobby or ""
            interest = profile.interest or ""
            keyword = interest or hobby  # keyword for external fetch

            personal = products.filter(
                Q(category__icontains=hobby) |
                Q(description__icontains=hobby) |
                Q(category__icontains=interest) |
                Q(description__icontains=interest)
            )
        except UserProfile.DoesNotExist:
            personal = []

    # Deduplicate internal
    combined = list(content_based) + list(collaborative) + list(personal)
    seen = set()
    final_internal = []
    for p in combined:
        if p.id not in seen:
            seen.add(p.id)
            final_internal.append(p)

    internal_top = final_internal[:top_n]

    # -----------------------
    # External recommendations
    # -----------------------
    keyword = keyword or (target.category if target else "electronics")

    external = []
    try:
        external += scrape_jumia(keyword)  # ✅ real scraping
    except Exception as e:
        print("Jumia scrape failed:", e)

    # Keep mocks for now
    external += fetch_from_konga(keyword)
    external += fetch_from_amazon(keyword)

    return {
        "internal": list(internal_top),
        "external": external
    }
