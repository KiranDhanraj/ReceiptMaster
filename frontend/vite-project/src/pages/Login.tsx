import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api, { setTokens } from "../services/api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    setError("");
    try {
      const response = await api.post("/login", {
        email,
        password,
      });

      const { access_token, refresh_token, username } = response.data;
      setTokens(access_token, refresh_token, username);
      navigate("/upload");
    } catch (err) {
      setError("Login failed");
    }
  };

  return (
    <div>
      <h1>Login</h1>

      <input
        placeholder="email"
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleLogin}>
        Login
      </button>

      {error ? <p>{error}</p> : null}
    </div>
  );
}