import { useNavigate } from "react-router-dom"; 
import "../styles/manageLessons.css";
import UserInfo from "../components/UserInfo"; 

export default function UserDashboard() {
  const navigate = useNavigate();

  return (
    <div className="manage-container">
      <UserInfo /> 

      <div className="manage-buttons">
        <button onClick={() => navigate("/chat")}>Chat Agent</button>
        <button onClick={() => navigate("/book")}>Book a New Lesson</button>
        <button onClick={() => navigate("/my-lessons")}>Manage My Lessons</button>
        </div>
    </div>
  );
}
