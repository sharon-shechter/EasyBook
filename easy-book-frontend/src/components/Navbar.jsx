import { Link } from "react-router-dom";
import "../styles/navbar.css";

export default function Navbar() {
  return (
    <nav className="navbar">
      <h1 className="logo">Easy Book</h1>
      <div className="nav-links">
        <Link to="/login">Log in</Link>
        <Link to="/signup">Sign Up</Link>
      </div>
    </nav>
  );
}
