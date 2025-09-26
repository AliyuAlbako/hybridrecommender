// src/components/ProductCard.jsx
import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext";
import StarRating from "./StarRating";

export default function ProductCard({ product }) {
  const { addToCart } = useCart();

  return (
    <div className="card">
      <img
        className="product--image"
        src={product.image_url || "/images/placeholder.png"}
        alt={product.name}
      />

      <h3>
        <Link to={`/product/${product.id}`}>{product.name}</Link>
      </h3>

      {/* Show stars if avg_rating is present */}
      {/* {product.avg_rating !== undefined && (
        <StarRating rating={product.avg_rating} />
      )} */}
      <div className="rating-display">
                  <StarRating rating={product.avg_rating || 0} />
                  <span className="rating-text">
                    {product.avg_rating ? product.avg_rating.toFixed(1) : "No ratings yet"}
                  </span>
                </div>

      <p>
        {product.description?.substring(0, 90)}
        {product.description?.length > 90 ? "..." : ""}
      </p>
      <p className="price">₦{product.price}</p>

      <div style={{ display: "flex", gap: "10px" }}>
        <Link to={`/product/${product.id}`} className="card-button">
          View
        </Link>
        <button
          onClick={() => addToCart(product.id)}
          className="card-button"
          style={{ backgroundColor: "#4CAF50", color: "white" }}
        >
          Add to Cart
        </button>
      </div>
    </div>
  );
}
