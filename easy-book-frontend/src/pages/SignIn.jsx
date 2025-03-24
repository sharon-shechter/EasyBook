import { useState } from "react";

export default function SignIn() {
  const [formData, setFormData] = useState({ email: "", password: "" });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/users/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
  
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Login failed");
      }
  
      const token = await response.text(); // assuming FastAPI returns the token as plain text
      localStorage.setItem("token", token); // store JWT token
      alert("Login successful!");
  
      // optionally: redirect to home or another page
      // navigate("/"); <-- if using useNavigate from react-router
    } catch (err) {
      console.error("Login error:", err);
      alert("Login failed: " + err.message);
    }
  };

  return (
    <div>
      <h2>Sign In</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        /><br />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        /><br />
        <button type="submit">Sign In</button>
      </form>
    </div>
  );
}