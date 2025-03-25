import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import UserInfo from "../components/UserInfo";
import "../styles/editProfile.css";

export default function EditProfile() {
  const [userId, setUserId] = useState(0);
  const [showConfirm, setShowConfirm] = useState(false);
  const token = localStorage.getItem("token");
  const email = localStorage.getItem("userEmail");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserId = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/users/get_user/${email}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) throw new Error("Failed to fetch user data");

        const data = await response.json();
        setUserId(parseInt(data.user_id));
        } catch (err) {
        console.error("Failed to get user ID:", err);
      }
    };

    fetchUserId();
  }, [email, token]);

  const deleteAccount = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/users/delete/${userId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) throw new Error("Failed to delete user");

      localStorage.clear();
      navigate("/");
    } catch (err) {
      console.error("Error deleting user:", err);
      alert("Something went wrong while deleting your account.");
    }
  };

  return (
    <div className="edit-profile-container">
      <UserInfo />
      <h1>Edit Profile</h1>

      <div className="edit-buttons">
        <button onClick={() => alert("Feature coming soon!")}>🛠️ Update Profile</button>
        <button className="delete-btn" onClick={() => setShowConfirm(true)}>🗑️ Delete Profile</button>
      </div>

      {showConfirm && (
        <div className="confirmation-overlay">
          <div className="confirmation-box">
            <p>Are you sure you want to delete your profile?</p>
            <div className="confirmation-actions">
              <button className="cancel-btn" onClick={() => setShowConfirm(false)}>Cancel</button>
              <button className="confirm-btn" onClick={deleteAccount}>Yes, Delete</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
