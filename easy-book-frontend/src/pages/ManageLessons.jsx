import { useEffect, useState } from "react";
import "../styles/manageLessons.css";

export default function ManageLessons() {
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      const email = localStorage.getItem("userEmail");
      const token = localStorage.getItem("token");
      try {
        const response = await fetch(`http://127.0.0.1:8000/users/get_user/${email}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await response.json();
        console.log(data);
        setUserData(data);
      } catch (err) {
        console.error("Failed to fetch user data:", err);
      }
    };
    fetchUserData();
  }, []);

  return (
    <div className="manage-container">
      {userData ? (
        <div className="user-card">
          <h2>Hello {userData.first_name} 👋</h2>
          <div className="manage-buttons">
            <button>Chat Agent</button>
            <button>Book a New Lesson</button>
            <button>Manage My Lessons</button>
          </div>
        </div>
      ) : (
        <p>Loading user data...</p>
      )}
    </div>
  );
}