"""
Nuora Product Scraper
Scrapes live product data from mynuora.com for pricing analysis.
"""

import json
import os
import re
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

from config.settings import PRODUCTS_DIR


class NuoraScraper:
    """Scrapes product data from mynuora.com."""

    BASE_URL = "https://mynuora.com"
    PRODUCTS = {
        "vaginal_probiotic": "/products/feminine-balance-gummies-1",
        "gut_ritual": "/products/gut-capsule",
    }
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    }

    def __init__(self):
        if not HAS_DEPS:
            print("[scraper] requests/beautifulsoup4 not installed.")
            print("[scraper] Run: pip install requests beautifulsoup4")

    def scrape_product_json(self, product_handle):
        """
        Scrape product data using Shopify's .json endpoint.
        This is more reliable than parsing HTML.
        """
        if not HAS_DEPS:
            return None

        url = f"{self.BASE_URL}/products/{product_handle}.json"
        try:
            resp = requests.get(url, headers=self.HEADERS, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            return data.get("product", {})
        except Exception as e:
            print(f"[scraper] Failed to fetch {url}: {e}")
            return None

    def scrape_all_products(self):
        """Scrape all known Nuora products."""
        results = {}
        for name, path in self.PRODUCTS.items():
            handle = path.strip("/").split("/")[-1]
            print(f"[scraper] Fetching {name} ({handle})...")
            data = self.scrape_product_json(handle)
            if data:
                results[name] = self._process_product(data)
                print(f"[scraper] OK - {len(data.get('variants', []))} variants found")
            else:
                print(f"[scraper] Failed - using cached data")
        return results

    def _process_product(self, raw):
        """Process raw Shopify product data into structured format."""
        variants = []
        for v in raw.get("variants", []):
            variants.append({
                "id": v.get("id"),
                "title": v.get("title"),
                "price": float(v.get("price", 0)),
                "compare_at_price": float(v["compare_at_price"]) if v.get("compare_at_price") else None,
                "sku": v.get("sku"),
                "available": v.get("available", True),
                "option1": v.get("option1"),
                "option2": v.get("option2"),
            })

        return {
            "title": raw.get("title"),
            "handle": raw.get("handle"),
            "product_type": raw.get("product_type"),
            "vendor": raw.get("vendor"),
            "tags": raw.get("tags", []),
            "variants": variants,
            "variant_count": len(variants),
            "price_range": {
                "min": min(v["price"] for v in variants) if variants else 0,
                "max": max(v["price"] for v in variants) if variants else 0,
            },
            "scraped_at": datetime.now().isoformat(),
        }

    def save_to_disk(self, products):
        """Save scraped product data to JSON files."""
        os.makedirs(PRODUCTS_DIR, exist_ok=True)
        for name, data in products.items():
            filepath = os.path.join(PRODUCTS_DIR, f"{name}_live.json")
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
            print(f"[scraper] Saved {filepath}")

    def run(self):
        """Full scrape pipeline."""
        print("[scraper] Starting Nuora product scrape...")
        products = self.scrape_all_products()
        if products:
            self.save_to_disk(products)
            print(f"[scraper] Done - {len(products)} products scraped")
        else:
            print("[scraper] No products scraped - check network connection")
        return products


if __name__ == "__main__":
    scraper = NuoraScraper()
    scraper.run()
