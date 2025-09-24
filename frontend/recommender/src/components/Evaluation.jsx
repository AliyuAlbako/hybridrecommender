import React, { useEffect, useState } from "react";
import api from "../api";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from "recharts";

export default function Evaluation() {
  const [results, setResults] = useState(null);

  useEffect(() => {
    fetchResults();
  }, []);

  async function fetchResults() {
    try {
      const res = await api.get("/api/evaluate/");
      setResults(res.data);
    } catch (err) {
      console.error("Failed to fetch evaluation results:", err);
    }
  }

  if (!results) return <p>Loading evaluation metrics...</p>;

  // Convert metrics into chart data
  const chartData = Object.entries(results).map(([metric, value]) => ({
    metric,
    value: Number(value),
  }));

  return (
    <div className="evaluation-page">
      <h2>📊 Recommendation System Evaluation</h2>

      {/* Table display */}
      <table className="metrics-table">
        <thead>
          <tr>
            <th>Metric</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(results).map(([metric, value]) => (
            <tr key={metric}>
              <td>{metric}</td>
              <td>{value}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Chart display */}
      <div style={{ width: "100%", height: 400, marginTop: "2rem" }}>
        <ResponsiveContainer>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="metric" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="value" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
