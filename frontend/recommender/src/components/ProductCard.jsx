
import { Link } from "react-router-dom";

export default function ProductCard({ product }) {
  return (
    <div className="card">
      <img className="product--image" src={product.image_url || "/images/placeholder.png"} alt={product.name} />
      <h3><Link to={`/product/${product.id}`}>{product.name}</Link></h3>
      <p>{product.description?.substring(0, 90)}{product.description?.length > 90 ? "..." : ""}</p>
      <p className="price">{product.price}</p>
      <p><strong>Source:</strong> {product.source}</p>
      <Link to={`/product/${product.id}`} className="card-button">View</Link>
    </div>
  );
}
