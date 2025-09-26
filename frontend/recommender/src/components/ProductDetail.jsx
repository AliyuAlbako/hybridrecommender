// src/components/ProductDetail.jsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";
import ProductCard from "./ProductCard";
import StarRating from "./StarRating";

export default function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [internalRecs, setInternalRecs] = useState([]);
  const [externalRecs, setExternalRecs] = useState([]);
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
      setInternalRecs(res.data.internal_recommendations || []);
      setExternalRecs(res.data.external_recommendations || []);
    } catch (err) {
      console.error("Recs error", err);
    }
  }

  async function recordView() {
    try {
      await api.post(`/api/products/${id}/interact/`, {
        interaction_type: "view",
        value: 1.0,
      });
    } catch (err) {}
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

          {/* ⭐ Average rating */}
          <div className="rating-display">
            <StarRating rating={product.avg_rating || 0} />
            <span className="rating-text">
              {product.avg_rating
                ? product.avg_rating.toFixed(1)
                : "No ratings yet"}
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

      {/* Internal recommendations */}
      <h3>Recommended from our store</h3>
      <div className="card-container">
        {internalRecs.length ? (
          internalRecs.map((rec) => (
            <ProductCard key={rec.id} product={rec} />
          ))
        ) : (
          <p>No internal recommendations.</p>
        )}
      </div>

      <hr />

      {/* External recommendations */}
      <h3>Related products from other platforms</h3>
      <div className="card-container">
        {externalRecs.length ? (
          externalRecs.map((rec, idx) => (
            <div key={idx} className="card external-card">
              <img
                src={rec.image_url}
                alt={rec.name}
                className="product--image"
              />
              <h4>{rec.name}</h4>
              <p className="price">{rec.price}</p>
              <p style={{ fontSize: "12px", color: "#666" }}>
                Source: {rec.platform}
              </p>
              <a
                href={rec.url}
                target="_blank"
                rel="noreferrer"
                className="card-button"
                style={{color: "white"}}
              >
                View on {rec.platform}
              </a>
            </div>
          ))
        ) : (
          <p>No external recommendations.</p>
        )}
      </div>

    </div>
  );
}
