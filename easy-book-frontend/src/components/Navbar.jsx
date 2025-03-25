import { Link } from "react-router-dom";
import "../styles/navbar.css";

export default function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/" className="logo">Easy Book</Link> 
      <div className="nav-links">
        <Link to="/about">About</Link> 
        <Link to="/contact">Contact Us</Link> 
      </div>
    </nav>
  );
}
