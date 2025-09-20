import React from "react";
import { Link, useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem("access");

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    navigate("/login");
  };

  return (
    <nav className="nav" style={{ padding: "10px 20px", background: "#fff", display:"flex", justifyContent:"space-between", alignItems:"center" }}>
      <div>
        <Link to="/" style={{ fontWeight: 700, fontSize: "18px" }}>Hybrid Recommender</Link>
      </div>

      <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
        <Link to="/">Products</Link>
        {isLoggedIn ? (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <button onClick={handleLogout} style={{ padding: "6px 10px" }}>Logout</button>
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
