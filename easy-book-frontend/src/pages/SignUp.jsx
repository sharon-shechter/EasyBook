import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function SignUp() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    phone_number: "",
    address: "",
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:8000/users/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Signup failed");
      }

      alert("Account created successfully!");
      navigate("/login"); 

    } catch (err) {
      console.error("Signup error:", err);
      alert("Signup failed: " + err.message);
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
