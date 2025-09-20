import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";
import ProductCard from "./ProductCard";

export default function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [rating, setRating] = useState("");

  useEffect(() => {
    fetchDetail();
    recordView();
    fetchRecommendations();
    // eslint-disable-next-line
  }, [id]);

  async function fetchDetail() {
    try {
      const res = await api.get(`/api/products/${id}/`);
      setProduct(res.data);
    } catch (err) {
      console.error(err);
    }
  }

  async function fetchRecommendations() {
    try {
      // Endpoint expected to return list of products
      const res = await api.get(`/api/products/${id}/recommendations/`);
      setRecommendations(res.data.recommendations || res.data);
    } catch (err) {
      console.error("Recs error", err);
    }
  }

  async function recordView() {
    try {
      await api.post(`/api/products/${id}/interact/`, {
        interaction_type: "view",
        value: 1.0
      });
    } catch (err) {
      // ignore failure if endpoint absent
    }
  }

  async function submitRating() {
    if (!rating) return;
    try {
      await api.post(`/api/products/${id}/rate/`, { rating: Number(rating) });
      alert("Thanks for rating!");
      setRating("");
    } catch (err) {
      console.error(err);
    }
  }

  if (!product) return <p>Loading product...</p>;

  return (
    <div>
      <div className="card" style={{ maxWidth: 800 }}>
        <img src={product.image_url || "/images/placeholder.png"} alt={product.name} className="product--image" />
        <h2>{product.name}</h2>
        <p>{product.description}</p>
        <p className="price">{product.price}</p>
        <p><strong>Source:</strong> {product.source}</p>

        <div style={{ marginTop: 12 }}>
          <input type="number" min="1" max="5" value={rating} onChange={(e) => setRating(e.target.value)} placeholder="Rate 1-5" />
          <button onClick={submitRating}>Submit Rating</button>
        </div>
      </div>

      <hr />

      <h3>Recommended products</h3>
      <div className="card-container">
        {recommendations.length ? recommendations.map(rec => <ProductCard key={rec.id} product={rec} />) : <p>No recommendations.</p>}
      </div>
    </div>
  );
}
