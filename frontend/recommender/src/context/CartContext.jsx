import { createContext, useContext, useState, useEffect } from "react";
import api from "../api";

const CartContext = createContext();

export function CartProvider({ children }) {
  const [cartCount, setCartCount] = useState(0);

  // Load cart count on mount
  useEffect(() => {
    const fetchCart = async () => {
      try {
        const res = await api.get("/api/cart/");
        const total = res.data.reduce((sum, item) => sum + item.quantity, 0);
        setCartCount(total);
      } catch (err) {
        console.error("Failed to load cart:", err);
      }
    };
    fetchCart();
  }, []);

  const addToCart = async (productId) => {
    try {
      await api.post("/api/cart/add/", { product_id: productId, quantity: 1 });
      setCartCount((prev) => prev + 1); // update immediately
    } catch (err) {
      console.error("Add to cart failed:", err);
    }
  };

  const value = { cartCount, addToCart };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart() {
  return useContext(CartContext);
}
