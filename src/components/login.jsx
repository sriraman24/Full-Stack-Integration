import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaEye, FaEyeSlash } from "react-icons/fa";


function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
  fetch("http://localhost:5000/orders", {
    credentials: "include",
  }).then((res) => {
    if (res.status !== 401) {
      navigate("/orders");
    }
  });
}, []);


  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("http://localhost:5000/login", {                     // calling backend api of login from frontend
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ username, password }),
      });


      if (!response.ok) {
        const data = await response.json();                                             // 200 ok
        setError(data.error);
        return;
      }
      alert("Login successful");
      navigate("/orders");
                                                                                
    } catch {
      setError("Backend not reachable");
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
     <div style={{ position: "relative", width: "250px" }}>
  <input
    placeholder="Password"
    type={showPassword ? "text" : "password"}
    value={password}
    onChange={(e) => setPassword(e.target.value)}
    // style={{ width: "100%", paddingRight: "35px" }}
  />

  <span
    onClick={() => setShowPassword(!showPassword)}
    style={{
      position: "absolute",
      right: "90px",
      top: "50%",
      transform: "translateY(-40%)",
      cursor: "pointer",
      userSelect: "none",
    }}
  >
    {showPassword ? <FaEyeSlash size={16} /> : <FaEye size={16} />}
  </span>
</div>

      <button type="submit">Login</button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}

export default Login;