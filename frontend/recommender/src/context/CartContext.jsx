// src/context/CartContext.jsx
import { createContext, useContext, useState, useEffect } from "react";
import api from "../api";

const CartContext = createContext();

export function CartProvider({ children }) {
  const [cart, setCart] = useState([]);
  const [cartCount, setCartCount] = useState(0);

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const res = await api.get("/api/cart/");
      setCart(res.data);
      const total = res.data.reduce((sum, item) => sum + item.quantity, 0);
      setCartCount(total);
    } catch (err) {
      console.error("Failed to load cart:", err);
    }
  };

  const addToCart = async (productId) => {
    try {
      await api.post("/api/cart/add/", { product_id: productId, quantity: 1 });
      fetchCart();
    } catch (err) {
      console.error("Add to cart failed:", err);
    }
  };

  const removeFromCart = async (itemId) => {
    try {
      await api.delete(`/api/cart/${itemId}/`);
      fetchCart();
    } catch (err) {
      console.error("Remove failed:", err);
    }
  };

  const updateQuantity = async (itemId, quantity) => {
    try {
      await api.patch(`/api/cart/${itemId}/`, { quantity });
      fetchCart();
    } catch (err) {
      console.error("Update quantity failed:", err);
    }
  };

  const clearCart = async () => {
    try {
      await api.post("/api/cart/clear/");
      setCart([]);
      setCartCount(0);
    } catch (err) {
      console.error("Clear failed:", err);
    }
  };

  const checkout = async () => {
    try {
      const res = await api.post("/api/cart/checkout/");
      clearCart(); // empty cart after successful checkout
      return res.data.order; // return order summary
    } catch (err) {
      console.error("Checkout failed:", err);
      throw err;
    }
  };

  const value = {
    cart,
    cartCount,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    checkout,
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart() {
  return useContext(CartContext);
}
