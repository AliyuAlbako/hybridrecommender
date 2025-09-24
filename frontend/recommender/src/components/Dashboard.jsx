// src/components/Dashboard.jsx
import React, { useEffect, useState } from "react";
import api from "../api";

export default function Dashboard() {
  const [profile, setProfile] = useState({ hobby: "", interest: "" });
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchProfile();
  }, []);

  async function fetchProfile() {
    try {
      const res = await api.get("/api/profile/");
      setProfile(res.data);
    } catch (err) {
      console.error("Failed to load profile:", err);
    }
  }

  async function updateProfile(e) {
    e.preventDefault();
    try {
      await api.put("/api/profile/", profile);
      setMessage("Profile updated successfully!");
    } catch (err) {
      console.error("Failed to update profile:", err);
      setMessage("Update failed.");
    }
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>Dashboard</h2>
      <form onSubmit={updateProfile} style={{ display: "flex", flexDirection: "column", gap: "10px", maxWidth: "400px" }}>
        <label>
          Hobby:
          <input
            type="text"
            name="hobby"
            value={profile.hobby}
            onChange={(e) => setProfile({ ...profile, hobby: e.target.value })}
          />
        </label>
        <label>
          Interest:
          <input
            type="text"
            name="interest"
            value={profile.interest}
            onChange={(e) => setProfile({ ...profile, interest: e.target.value })}
          />
        </label>
        <button type="submit">Save</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}
