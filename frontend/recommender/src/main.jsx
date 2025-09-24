import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./assets/css/styles.css";
import { CartProvider } from "./context/CartContext";

createRoot(document.getElementById("root")).render(
  <CartProvider>
    <App />
  </CartProvider>
);
