import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/login";
import Orders from "./components/orders";
import ProtectedRoute from "./components/protectedroute";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />

      <Route path="/login" element={<Login />} />

      <Route
        path="/orders"
        element={
          <ProtectedRoute>
            <Orders />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

export default App;
