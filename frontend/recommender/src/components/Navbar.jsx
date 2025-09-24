// src/components/Navbar.jsx
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
        borderBottom: "1px solid #eee",
      }}
    >
      <div>
        <Link to="/" style={{ fontWeight: 700, fontSize: "18px" }}>
          Hybrid Recommender
        </Link>
      </div>

      <div style={{ display: "flex", gap: "15px", alignItems: "center" }}>
        <Link to="/">Products</Link>
        {isLoggedIn ? (
          <>
            <Link to="/dashboard">Dashboard</Link>

            {/* ✅ Cart with badge */}
            <Link to="/cart" style={{ position: "relative" }}>
              🛒 Cart
              {cartCount > 0 && (
                <span
                  style={{
                    position: "absolute",
                    top: "-6px",
                    right: "-12px",
                    background: "red",
                    color: "white",
                    borderRadius: "50%",
                    padding: "2px 7px",
                    fontSize: "12px",
                    fontWeight: "bold",
                  }}
                >
                  {cartCount}
                </span>
              )}
            </Link>

            <Link to="/orders">My Orders</Link>
            <button onClick={handleLogout} style={{ padding: "6px 10px" }}>
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
