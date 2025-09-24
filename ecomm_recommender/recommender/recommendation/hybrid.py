# recommender/recommendation/hybrid.py

from ..models import Product, UserProfile, Rating, UserInteraction
from django.db.models import Q
import requests


def fetch_from_jumia(category_or_keyword):
    """
    Fetch external products from Jumia.
    (Currently mocked because Jumia doesn’t provide open API)
    """
    # Example: in real case you would send request to a scraping microservice or API
    # For now, return mocked results
    return [
        {
            "platform": "Jumia",
            "name": "Easypie 20000mAh Power Bank",
            "price": "₦15,000",
            "url": "https://www.jumia.com.ng/easypie-easypie-20000mah-dual-fast-charge-64w-type-c-and-micro-usb-portable-power-bank-404295118.html",
            "image_url": "https://ng.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/18/592404/1.jpg",
        }
    ]


def fetch_from_konga(category_or_keyword):
    """Mock Konga recommendations"""
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
    """Mock Amazon recommendations"""
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
    - External products from Jumia, Konga, Amazon
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
        content_based = products

    collaborative_ids = []
    if product_id:
        interactions = UserInteraction.objects.filter(product_id=product_id)
        user_ids = interactions.values_list("user_id", flat=True)
        collaborative_ids = UserInteraction.objects.filter(user_id__in=user_ids).values_list("product_id", flat=True)

    collaborative = products.filter(id__in=collaborative_ids)

    personal = []
    keyword = None
    if user_id:
        try:
            profile = UserProfile.objects.get(user_id=user_id)
            hobby = profile.hobby or ""
            interest = profile.interest or ""
            keyword = interest or hobby  # use for external fetch

            personal = products.filter(
                Q(category__icontains=hobby) |
                Q(description__icontains=hobby) |
                Q(category__icontains=interest) |
                Q(description__icontains=interest)
            )
        except UserProfile.DoesNotExist:
            personal = []

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
    keyword = keyword or (target.category if product_id else "electronics")

    external = []
    external += fetch_from_jumia(keyword)
    external += fetch_from_konga(keyword)
    external += fetch_from_amazon(keyword)

    return {
        "internal": list(internal_top),
        "external": external
    }
