import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/login";
import Orders from "./components/orders";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/orders" element={<Orders />} />
    </Routes>
  );
}

export default App;

