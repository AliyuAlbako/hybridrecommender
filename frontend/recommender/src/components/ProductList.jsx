import React, { useEffect, useState } from "react";
import api from "../api";
import ProductCard from "./ProductCard";

export default function ProductList() {
  const [products, setProducts] = useState([]);
  const [q, setQ] = useState("");
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    fetchProducts();
  }, []);

  async function fetchProducts() {
    try {
      const res = await api.get("/api/products/");
      setProducts(res.data);
    } catch (err) {
      console.error(err);
    }
  }

  const handleSearchChange = (e) => {
    const value = e.target.value;
    setQ(value);
    if (!value) {
      setSuggestions([]);
      return;
    }
    const filtered = products.filter(p => p.name.toLowerCase().includes(value.toLowerCase()));
    setSuggestions(filtered.slice(0, 6));
  };

  const displayed = q ? products.filter(p => p.name.toLowerCase().includes(q.toLowerCase())) : products;

  return (
    <div>
      <h2>Products</h2>
      <div style={{ marginBottom: 12 }}>
        <input type="text" placeholder="Search products..." value={q} onChange={handleSearchChange} />
      </div>

      {suggestions.length > 0 && (
        <div style={{ position: "absolute", background: "#fff", border: "1px solid #ccc", zIndex: 1000 }}>
          {suggestions.map(s => (
            <div key={s.id} style={{ padding: 8 }}>
              <a href={`/product/${s.id}`}>{s.name}</a>
            </div>
          ))}
        </div>
      )}

      <div className="card-container">
        {displayed.length ? displayed.map(p => <ProductCard key={p.id} product={p} />) : <p>No products.</p>}
      </div>
    </div>
  );
}
