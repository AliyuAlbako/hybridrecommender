# recommender/recommendation/cache_utils.py
import os
import pickle
from django.conf import settings

CACHE_DIR = os.path.join(getattr(settings, "BASE_DIR", "."), "recommendation_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def save_cache(obj, name):
    path = os.path.join(CACHE_DIR, name)
    with open(path, "wb") as f:
        pickle.dump(obj, f)

def load_cache(name):
    path = os.path.join(CACHE_DIR, name)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

def clear_cache():
    for fname in os.listdir(CACHE_DIR):
        try:
            os.remove(os.path.join(CACHE_DIR, fname))
        except Exception:
            pass
