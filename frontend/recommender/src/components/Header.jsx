import React from "react";
import { Link } from "react-router-dom";
import "./Header.css"; // We'll style this later

const Header = () => {
  return (
    <header>
      <nav className="nav">
        <h5 className="logo">
          <Link to="/"><img src="/images/logo.jpg" height="70px" alt="Logo" /></Link>
        </h5>
        <ul className="nav-group">
          <li className="nav-item"><Link to="/">Home</Link></li>
          <li className="nav-item"><Link to="/about">About</Link></li>
          <li className="nav-item"><Link to="/feedbacks">Feedbacks</Link></li>
          <li className="nav-item"><Link to="/branches">Our Branches</Link></li>
          <li className="nav-item"><Link to="/contact">Contact Us</Link></li>
        </ul>
        <div className="reg">
          <button>Register</button>
          <button>Login</button>
        </div>
      </nav>
      <div className="head">
        <h1>Hybrid Sales</h1>
      </div>
    </header>
  );
};

export default Header;
