# recommender/recommendation/external_sources.py

import requests

def fetch_jumia_products(query, limit=5):
    """
    Simulate Jumia API fetch (replace with real API/web scraping later).
    Right now we mock response.
    """
    return [
        {
            "id": f"jumia_{i}",
            "name": f"Jumia {query} Product {i}",
            "description": f"External {query} product from Jumia platform.",
            "price": "N5,000",
            "image_url": "https://via.placeholder.com/200",
            "source": "Jumia",
            "product_url": "https://www.jumia.com.ng/"
        }
        for i in range(1, limit + 1)
    ]


def fetch_konga_products(query, limit=5):
    return [
        {
            "id": f"konga_{i}",
            "name": f"Konga {query} Product {i}",
            "description": f"External {query} product from Konga platform.",
            "price": "N7,500",
            "image_url": "https://via.placeholder.com/200",
            "source": "Konga",
            "product_url": "https://www.konga.com/"
        }
        for i in range(1, limit + 1)
    ]


def fetch_amazon_products(query, limit=5):
    return [
        {
            "id": f"amazon_{i}",
            "name": f"Amazon {query} Product {i}",
            "description": f"External {query} product from Amazon platform.",
            "price": "$20",
            "image_url": "https://via.placeholder.com/200",
            "source": "Amazon",
            "product_url": "https://www.amazon.com/"
        }
        for i in range(1, limit + 1)
    ]


def fetch_external_recommendations(query, limit=3):
    """
    Get cross-platform products for a given query/category.
    """
    jumia = fetch_jumia_products(query, limit)
    konga = fetch_konga_products(query, limit)
    amazon = fetch_amazon_products(query, limit)

    return jumia + konga + amazon
