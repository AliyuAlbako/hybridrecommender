import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";
import ProductCard from "./ProductCard";
import StarRating from "./StarRating"; // ⭐ Import star rating component

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
      // ignore failure
    }
  }

  async function submitRating() {
    if (!rating) return;
    try {
      await api.post(`/api/products/${id}/rate/`, { rating: Number(rating) });
      alert("Thanks for rating!");
      setRating("");
      fetchDetail(); // refresh product to update avg rating
    } catch (err) {
      console.error(err);
    }
  }

  if (!product) return <p>Loading product...</p>;

  return (
    <div className="detail-page">
      <div className="detail-card">
        <img
          src={product.image_url || "/images/placeholder.png"}
          alt={product.name}
          className="detail-image"
        />
        <div className="detail-info">
          <h2>{product.name}</h2>
          <p className="detail-description">{product.description}</p>
          <p className="price">₦{product.price}</p>

          {/* ⭐ Show average rating */}
          <div className="rating-display">
            <StarRating rating={product.avg_rating || 0} />
            <span className="rating-text">
              {product.avg_rating ? product.avg_rating.toFixed(1) : "No ratings yet"}
            </span>
          </div>

          {/* ⭐ Rating form */}
          <div className="rating-form">
            <input
              type="number"
              min="1"
              max="5"
              value={rating}
              onChange={(e) => setRating(e.target.value)}
              placeholder="Rate 1-5"
            />
            <button onClick={submitRating}>Submit Rating</button>
          </div>
        </div>
      </div>

      <hr />

      <h3>Recommended products</h3>
      <div className="card-container">
        {recommendations.length
          ? recommendations.map((rec) => <ProductCard key={rec.id} product={rec} />)
          : <p>No recommendations.</p>}
      </div>
    </div>
  );
}
