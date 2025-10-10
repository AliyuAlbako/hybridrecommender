import requests
import time
import json
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from ...models import Product

# Define the keywords (hobbies + interests)
HOBBIES = ["Reading", "Sports", "Gaming", "Travel", "Music", "Art"]
INTERESTS = ["Tech", "Fashion", "Electronics", "Books", "Home Decor", "Health"]
BASE_URL = "https://www.jumia.com.ng/catalog/?q="


def scrape_jumia_products(keyword, max_items=5):
    """Scrape Jumia search results for a specific keyword."""
    print(f"🔍 Scraping Jumia for keyword: {keyword}")
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"{BASE_URL}{keyword.replace(' ', '+')}"
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    products = []
    for product in soup.select("article.prd._fb.col.c-prd")[:max_items]:
        name_tag = product.select_one("h3.name")
        price_tag = product.select_one("div.prc")
        image_tag = product.select_one("img.img")
        link_tag = product.select_one("a.core")

        if not (name_tag and price_tag and image_tag and link_tag):
            continue

        name = name_tag.text.strip()
        price = price_tag.text.strip().replace("₦", "").replace(",", "")
        image_url = image_tag.get("data-src") or image_tag.get("src")
        product_url = "https://www.jumia.com.ng" + link_tag.get("href")

        products.append({
            "name": name,
            "category": keyword,
            "price": price or 0,
            "image_url": image_url,
            "source": "Jumia",
            "product_url": product_url,
        })

    print(f"✅ Found {len(products)} items for '{keyword}'")
    return products


class Command(BaseCommand):
    help = "Scrapes real Jumia products for hobbies and interests, avoids duplicates, and saves JSON backup."

    def handle(self, *args, **options):
        keywords = HOBBIES + INTERESTS
        added_count = 0
        all_scraped = []

        for keyword in keywords:
            existing = Product.objects.filter(category__iexact=keyword).exists()
            if existing:
                print(f"⚠️ Skipping '{keyword}' — already populated.")
                continue

            try:
                products = scrape_jumia_products(keyword)
                for p in products:
                    obj, created = Product.objects.get_or_create(
                        name=p["name"],
                        defaults=p
                    )
                    if created:
                        added_count += 1
                        all_scraped.append(p)
                time.sleep(2)  # polite delay
            except Exception as e:
                print(f"❌ Error scraping {keyword}: {e}")

        # Save backup file
        if all_scraped:
            with open("scraped_products_backup.json", "w", encoding="utf-8") as f:
                json.dump(all_scraped, f, ensure_ascii=False, indent=2)
            print(f"💾 Backup saved: scraped_products_backup.json")

        self.stdout.write(
            self.style.SUCCESS(f"✅ Finished! Added {added_count} new products to the database.")
        )
