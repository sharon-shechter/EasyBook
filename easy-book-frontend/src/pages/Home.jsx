import { useNavigate } from "react-router-dom";
import "../styles/home.css";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <h1>Welcome to Easy Book</h1>
      <div className="home-buttons">
        <button onClick={() => navigate("/login")}>Log In</button>
        <button onClick={() => navigate("/signup")}>Sign Up</button>
      </div>

      <div className="recommendations-wrapper">
        <div className="recommendations-track">
          <div className="recommendation-box">"Sharon helped me pass my math final!" – Lior</div>
          <div className="recommendation-box">"Explained recursion better than my CS professor 😅" – Tal</div>
          <div className="recommendation-box">"The Zoom lessons are super clear and helpful." – Maya</div>
          <div className="recommendation-box">"Amazing tutor. Professional and patient!" – Ron</div>
          <div className="recommendation-box">"Finally got into coding thanks to Sharon!" – Inbar</div>
        </div>
      </div>
    </div>
  );
}
