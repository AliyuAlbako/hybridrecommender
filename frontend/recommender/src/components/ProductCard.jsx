import { Link } from "react-router-dom";
import StarRating from "./StarRating";

export default function ProductCard({ product, handleAddToCart }) {
  return (
    <div className="card">
      <img
        className="product--image"
        src={product.image_url || "/images/placeholder.png"}
        alt={product.name}
      />
      <h3><Link to={`/product/${product.id}`}>{product.name}</Link></h3>
      <p>
        {product.description?.substring(0, 90)}
        {product.description?.length > 90 ? "..." : ""}
      </p>
      <p className="price">${product.price}</p>
      <StarRating rating={product.avg_rating || 0} />   {/* ⭐ average rating */}
      <p><strong>Source:</strong> {product.source}</p>

      <div className="card-buttons">
        <Link to={`/product/${product.id}`} className="card-button view">View</Link>
        <button className="card-button cart" onClick={() => handleAddToCart(product)}>
          Add to Cart
        </button>
      </div>
    </div>
  );
}
