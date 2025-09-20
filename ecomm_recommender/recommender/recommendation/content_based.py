# recommender/recommendation/content_based.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..models import Product
from .cache_utils import load_cache, save_cache

CACHE_NAME = "content_model.pkl"

def build_content_model(max_features=5000):
    products = Product.objects.all().values("id", "name", "description", "category")
    df = pd.DataFrame(list(products))
    if df.empty:
        model = {"df": df, "cosine_sim": None, "tfidf": None}
        save_cache(model, CACHE_NAME)
        return model

    # combine text fields
    df["text"] = (df["name"].fillna("") + " " + df["description"].fillna("") + " " + df["category"].fillna("")).astype(str)

    tfidf = TfidfVectorizer(stop_words="english", max_features=max_features)
    tfidf_matrix = tfidf.fit_transform(df["text"])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    model = {"df": df.reset_index(drop=True), "cosine_sim": cosine_sim, "tfidf": tfidf}
    save_cache(model, CACHE_NAME)
    return model

def get_content_model():
    model = load_cache(CACHE_NAME)
    if model is None:
        model = build_content_model()
    return model

def get_content_recommendations(product_id, top_n=10):
    model = get_content_model()
    df = model["df"]
    cosine_sim = model["cosine_sim"]
    if df.empty or cosine_sim is None:
        return []

    if product_id not in df["id"].values:
        return []

    idx = int(df.index[df["id"] == product_id][0])
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1: top_n + 1]
    product_indices = [i for i, _ in sim_scores]
    recommended_ids = df.iloc[product_indices]["id"].tolist()
    return recommended_ids
