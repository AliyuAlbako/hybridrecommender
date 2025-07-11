import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..models import Product

def get_content_based_recommendations(product_id, top_n=5):
    # Fetch product data from the database
    products = Product.objects.all()
    df = pd.DataFrame(list(products.values('id', 'name', 'description', 'source')))

    if df.empty:
        # No products in the database
        return Product.objects.none()

    # Vectorize the product descriptions using TF-IDF
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['description'])

    # Compute cosine similarity between all products
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Find the index of the product with the given product_id
    idx = df.index[df['id'] == product_id].tolist()
    if not idx:
        # Product ID not found
        return Product.objects.none()

    idx = idx[0]

    # Get similarity scores for this product with all others
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort products based on similarity score (highest first), skip the product itself
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    # Get the product IDs of the top N similar products
    product_indices = [i[0] for i in sim_scores]
    recommended_ids = df.iloc[product_indices]['id'].tolist()

    # Query and return the actual product objects
    return Product.objects.filter(id__in=recommended_ids)

