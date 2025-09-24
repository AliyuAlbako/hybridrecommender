// src/components/Orders.jsx
import React, { useEffect, useState } from "react";
import api from "../api";

export default function Orders() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const res = await api.get("/api/orders/");
        setOrders(res.data);
      } catch (err) {
        console.error("Failed to fetch orders:", err);
      }
    };
    fetchOrders();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>Your Orders</h2>
      {orders.length === 0 ? (
        <p>No past orders yet.</p>
      ) : (
        orders.map((order) => (
          <div
            key={order.id}
            style={{
              marginBottom: "20px",
              padding: "15px",
              border: "1px solid #ddd",
              borderRadius: "8px",
              background: "#fff",
            }}
          >
            <h4>
              Order #{order.id} — {new Date(order.created_at).toLocaleString()}
            </h4>
            <p>
              <strong>Total:</strong> ${order.total} {order.currency}
            </p>
            <ul>
              {order.items.map((item, idx) => (
                <li key={idx}>
                  {item.product} — {item.quantity} × ${item.unit_price} = ${item.total_price}
                </li>
              ))}
            </ul>
          </div>
        ))
      )}
    </div>
  );
}
