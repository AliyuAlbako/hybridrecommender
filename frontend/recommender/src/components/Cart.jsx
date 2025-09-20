// src/components/Cart.jsx
import React from "react";
import { useCart } from "../context/CartContext";

const Cart = () => {
  const { cart, removeFromCart, clearCart } = useCart();

  const total = cart.reduce((sum, item) => sum + (item.price || 0), 0);

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
                }}
              >
                <div style={{ flex: 1 }}>
                  <h4 style={{ margin: 0 }}>{item.name}</h4>
                  <p style={{ margin: "4px 0", color: "#555" }}>
                    ${item.price}
                  </p>
                </div>

                <button
                  onClick={() => removeFromCart(item.id)}
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

          <button
            onClick={clearCart}
            style={{
              padding: "10px 15px",
              marginTop: "10px",
              background: "#f44336",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Clear Cart
          </button>
        </>
      )}
    </div>
  );
};

export default Cart;
