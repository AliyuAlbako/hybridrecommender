// src/components/Cart.jsx
import React, { useState } from "react";
import { useCart } from "../context/CartContext";

const Cart = () => {
  const { cart = [], removeFromCart, updateQuantity, clearCart, checkout } = useCart() || {};
  const [orderSummary, setOrderSummary] = useState(null);

  const total = (cart || []).reduce(
    (sum, item) => sum + (Number(item.product?.price) || 0) * item.quantity,
    0
  );

  const handleCheckout = async () => {
    try {
      const summary = await checkout();
      setOrderSummary(summary);
      alert("Order placed successfully!");
    } catch (err) {
      alert("Checkout failed. Please try again.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Your Cart</h2>

      {cart.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <>
          <ul style={{ listStyle: "none", padding: 0 }}>
            {cart.map((item) => (
              <li
                key={item.id}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  padding: "10px",
                  borderBottom: "1px solid #ddd",
                  background: "#fff",
                  borderRadius: "8px",
                  marginBottom: "10px",
                }}
              >
                <img
                  src={item.product?.image_url || "/images/placeholder.png"}
                  alt={item.product?.name}
                  style={{
                    width: "60px",
                    height: "60px",
                    objectFit: "cover",
                    borderRadius: "6px",
                    marginRight: "12px",
                  }}
                />

                <div style={{ flex: 1 }}>
                  <h4 style={{ margin: 0 }}>{item.product?.name}</h4>
                  <p style={{ margin: "4px 0", color: "#555" }}>
                    ${item.product?.price}
                  </p>

                  {/* Quantity Controls */}
                  <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                    <button
                      onClick={() => updateQuantity(item.id, item.quantity - 1)}
                      disabled={item.quantity <= 1}
                      style={{ padding: "4px 8px" }}
                    >
                      ➖
                    </button>
                    <span>{item.quantity}</span>
                    <button
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                      style={{ padding: "4px 8px" }}
                    >
                      ➕
                    </button>
                  </div>
                </div>

                <strong style={{ marginRight: "20px" }}>
                  ${(item.product?.price * item.quantity).toFixed(2)}
                </strong>

                <button
                  onClick={() => removeFromCart?.(item.id)}
                  style={{
                    padding: "6px 10px",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                    background: "#f8f8f8",
                    cursor: "pointer",
                  }}
                >
                  ❌ Remove
                </button>
              </li>
            ))}
          </ul>

          <h3 style={{ marginTop: "20px" }}>Total: ${total.toFixed(2)}</h3>

          <div style={{ display: "flex", gap: "10px", marginTop: "15px" }}>
            <button
              onClick={clearCart}
              style={{
                padding: "10px 15px",
                background: "#f44336",
                color: "white",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
              }}
            >
              Clear Cart
            </button>

            <button
              onClick={handleCheckout}
              style={{
                padding: "10px 15px",
                background: "#4CAF50",
                color: "white",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
              }}
            >
              Checkout
            </button>
          </div>

          {orderSummary && (
            <div style={{ marginTop: "20px", padding: "15px", background: "#f0f9f0", borderRadius: "8px" }}>
              <h4>Order Summary</h4>
              <ul>
                {orderSummary.items.map((it, idx) => (
                  <li key={idx}>
                    {it.name} x {it.quantity} = ${it.total_price}
                  </li>
                ))}
              </ul>
              <p><strong>Total Paid: ${orderSummary.total}</strong></p>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Cart;
