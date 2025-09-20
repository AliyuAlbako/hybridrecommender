import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";

const Navbar = () => {
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem("access");
  const { cartCount } = useCart();

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    navigate("/login");
  };

  return (
    <nav
      className="nav"
      style={{
        padding: "10px 20px",
        background: "#fff",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
      }}
    >
      {/* Logo / App Name */}
      <div>
        <Link
          to="/"
          style={{ fontWeight: 700, fontSize: "18px", textDecoration: "none" }}
        >
          Hybrid Recommender
        </Link>
      </div>

      {/* Links */}
      <div style={{ display: "flex", gap: "16px", alignItems: "center" }}>
        <Link to="/">Products</Link>
        <Link to="/cart">🛒 Cart ({cartCount})</Link>

        {isLoggedIn ? (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <button
              onClick={handleLogout}
              style={{
                padding: "6px 10px",
                border: "1px solid #ccc",
                borderRadius: "4px",
                background: "#f8f8f8",
                cursor: "pointer",
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/signup">Signup</Link>
            <Link to="/login">Login</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
