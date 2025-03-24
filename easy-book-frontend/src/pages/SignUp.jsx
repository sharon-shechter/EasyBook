import { useState } from "react";

export default function SignUp() {
  const [formData, setFormData] = useState({
    admin: false,
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    phone_number: "",
    address: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:8000/users/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Login failed");
      }

      const token = await response.text();
      localStorage.setItem("token", token);
      alert("Login successful!");
    } catch (err) {
      console.error("Login error:", err);
      alert("Login failed: " + err.message);
    }
  };


  return (
    <div>
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required /><br />
        <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required /><br />
        <input type="text" name="first_name" placeholder="First Name" value={formData.first_name} onChange={handleChange} required /><br />
        <input type="text" name="last_name" placeholder="Last Name" value={formData.last_name} onChange={handleChange} required /><br />
        <input type="text" name="phone_number" placeholder="Phone Number" value={formData.phone_number} onChange={handleChange} /><br />
        <input type="text" name="address" placeholder="Address" value={formData.address} onChange={handleChange} /><br />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}