import React from "react";
// import "..assets/css/StarRating.css";
export default function StarRating({ rating }) {
  // Round rating to nearest half (e.g. 3.5)
  const stars = [];
  const rounded = Math.round(rating * 2) / 2;

  for (let i = 1; i <= 5; i++) {
    if (i <= rounded) {
      stars.push(<span key={i} className="star filled">★</span>);
    } else if (i - 0.5 === rounded) {
      stars.push(<span key={i} className="star half">★</span>);
    } else {
      stars.push(<span key={i} className="star">★</span>);
    }
  }

  return <div className="star-rating">{stars}</div>;
}
