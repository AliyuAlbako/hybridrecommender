// src/components/Signup.jsx
import React, { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    hobby: "",
    interest: ""
  });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post("/api/register/", form); // ✅ fixed endpoint
      setMessage(res.data.message || "Signup successful. Please login.");
      setTimeout(() => navigate("/login"), 1200);
    } catch (err) {
      // ✅ more detailed error
      if (err.response?.data) {
        const errorMsg = Object.values(err.response.data).join(" ");
        setMessage(errorMsg);
      } else {
        setMessage("Signup failed. Check console.");
      }
      console.error("Signup error:", err);
    }
  };

  return (
    <div className="auth-container">
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit} className="auth-form">
        <input
          name="username"
          placeholder="Username"
          value={form.username}
          onChange={handleChange}
          required
        />
        <input
          name="email"
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
        />
        <input
          name="password"
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
        />
        <input
          name="hobby"
          placeholder="Your Hobby (e.g. Football, Music)"
          value={form.hobby}
          onChange={handleChange}
        />
        <input
          name="interest"
          placeholder="Your Interest (e.g. Fashion, Tech)"
          value={form.interest}
          onChange={handleChange}
        />
        <button type="submit">Register</button>
      </form>
      {message && <p className="auth-message">{message}</p>}
    </div>
  );
}
