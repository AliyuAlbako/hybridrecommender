import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProductList from "./components/ProductList";
import ProductDetail from "./components/ProductDetail";
import Signup from "./components/Signup";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import Cart from "./components/Cart";
import Orders from "./components/Orders";
import Evaluation from "./components/Evaluation";


export default function App() {
  return (
    <Router>
      <Navbar />
      <main style={{ padding: "20px" }}>
        <Routes>
          <Route path="/" element={<ProductList />} />
          <Route path="/product/:id" element={<ProductDetail />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/cart" element={<ProtectedRoute><Cart /></ProtectedRoute>} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/orders"element={<ProtectedRoute><Orders /></ProtectedRoute>}/>
          <Route path="/dashboard" element={<ProtectedRoute> <Dashboard /></ProtectedRoute> } />
           <Route path="/orders"element={<ProtectedRoute><Orders /></ProtectedRoute>}/>
           <Route path="/evaluation" element={<Evaluation />} />
        </Routes> 
     </main>
  </Router>
  );
}
