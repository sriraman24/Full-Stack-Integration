import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";

function protectedroute({ children }) {
  const [allowed, setAllowed] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/orders", {
      credentials: "include",
    })
      .then((res) => {
        if (res.status === 401) {
          setAllowed(false);
        } else {
          setAllowed(true);
        }
      })
      .catch(() => setAllowed(false));
  }, []);

  if (allowed === null) return <p>Checking authentication...</p>;

  return allowed ? children : <Navigate to="/login" replace />;
}

export default protectedroute;
