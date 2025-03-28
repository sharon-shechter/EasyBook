import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css"; 
const apiUrl = import.meta.env.VITE_API_URL;


export default function LogIn() {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${apiUrl}/users/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const text = await response.text();
        let errorMessage = "Login failed";
      
        try {
          const json = JSON.parse(text);
          errorMessage = json.detail || errorMessage;
        } catch {
          errorMessage = text || errorMessage;
        }
      
        throw new Error(errorMessage);
      }

      const data = await response.json();
      const token = data.access_token;
      localStorage.setItem("token", token);
      localStorage.setItem("userEmail", formData.email);
      alert("Login successful!");
      navigate("/dashboard");
    } catch (err) {
      console.error("Login error:", err);
      alert("Login failed: " + err.message);
    }
  };

  return (
    <div className="login-container">
      <h2>Sign In</h2>
      <form onSubmit={handleSubmit} className="login-form">
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit">Sign In</button>
      </form>
    </div>
  );
}
