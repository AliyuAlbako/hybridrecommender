# recommender/recommendation/external_scraper.py

import requests
from bs4 import BeautifulSoup


def scrape_jumia(keyword, max_results=5):
    """
    Scrape Jumia Nigeria search results for the given keyword.
    Returns a list of products (name, price, url, image).
    """
    url = f"https://www.jumia.com.ng/catalog/?q={keyword.replace(' ', '%20')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print("Jumia scrape failed:", e)
        return []

    soup = BeautifulSoup(r.text, "html.parser")

    cards = soup.select("article.prd._fb.col.c-prd")
    results = []
    for card in cards[:max_results]:
        name_tag = card.select_one("h3.name")
        price_tag = card.select_one(".prc")
        link_tag = card.select_one("a.core")
        img_tag = card.select_one("img.img")

        if not (name_tag and price_tag and link_tag and img_tag):
            continue

        results.append({
            "platform": "Jumia",
            "name": name_tag.get_text(strip=True),
            "price": price_tag.get_text(strip=True),
            "url": "https://www.jumia.com.ng" + link_tag["href"],
            "image_url": img_tag.get("data-src") or img_tag.get("src"),
        })

    return results
def scrape_konga(keyword, max_results=5):
    url = f"https://www.konga.com/catalogsearch/result/?q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    for item in soup.select("div.aisle-product-card")[:max_results]:
        try:
            name = item.select_one("h3.name") or item.select_one("span.name")
            price = item.select_one(".price") or item.select_one("span.product-price")
            link_tag = item.select_one("a")
            img_tag = item.select_one("img")

            results.append({
                "platform": "Konga",
                "name": name.get_text(strip=True) if name else "Unknown",
                "price": price.get_text(strip=True) if price else "N/A",
                "url": "https://www.konga.com" + link_tag["href"] if link_tag else "#",
                "image_url": img_tag["src"] if img_tag else "",
            })
        except Exception:
            continue
    return results


# ------------------------------
# Scraper for Amazon
# ------------------------------
def scrape_amazon(keyword, max_results=5):
    """
    Scrape Amazon search results.
    Note: Amazon has strong anti-scraping, so this may fail without proxies/headers.
    We'll keep a fallback in hybrid.py.
    """
    url = f"https://www.amazon.com/s?k={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36"
    }

    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    for item in soup.select("div.s-result-item")[:max_results]:
        try:
            name = item.select_one("span.a-text-normal")
            price = item.select_one("span.a-price-whole")
            link_tag = item.select_one("a.a-link-normal")
            img_tag = item.select_one("img.s-image")

            results.append({
                "platform": "Amazon",
                "name": name.get_text(strip=True) if name else "Unknown",
                "price": "$" + price.get_text(strip=True) if price else "N/A",
                "url": "https://www.amazon.com" + link_tag["href"] if link_tag else "#",
                "image_url": img_tag["src"] if img_tag else "",
            })
        except Exception:
            continue

    return results
