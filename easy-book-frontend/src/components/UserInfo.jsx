import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import '../styles/userInfo.css';
const apiUrl = import.meta.env.VITE_API_URL;


export default function UserInfo() {
  const [userData, setUserData] = useState(null);
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  const token = localStorage.getItem("token");
  const email = localStorage.getItem("userEmail");

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch(`${apiUrl}/users/get_user/${email}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) throw new Error("Failed to fetch user data");

        const data = await response.json();
        setUserData(data);
      } catch (err) {
        console.error("User info error:", err);
      }
    };

    fetchUserData();
  }, [email, token]);

  if (!userData) return null;

  return (
    <div className="floating-widget">
      <div className={`bubble ${open ? 'open' : ''}`} onClick={() => setOpen(!open)}>
        👋 Hello {userData.first_name}
        <span className="arrow">{open ? "⬇️" : "⬅️"}</span>
      </div>

      {open && (
        <div className="menu">
          <button onClick={() => navigate("/dashboard")}>🏠 Back to Dashboard</button>
          <button onClick={() => navigate("/profile/edit")}>🛠️ Edit Profile</button>

          <hr />

          <button onClick={() => {
            localStorage.clear();
            navigate("/login");
          }}>🚪 Log Out</button>
        </div>
      )}
    </div>
  );
}
