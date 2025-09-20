import React, { useEffect, useState } from "react";
import api from "../api";

export default function Dashboard() {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.get("/api/profile/");
        setProfile(res.data);
      } catch (err) {
        console.error("Profile fetch error", err);
      }
    };
    fetchProfile();
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      {profile ? (
        <div className="card">
          <p><strong>Username:</strong> {profile.username}</p>
          <p><strong>Email:</strong> {profile.email}</p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}
