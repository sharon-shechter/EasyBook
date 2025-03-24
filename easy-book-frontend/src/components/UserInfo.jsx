import { useEffect, useState } from "react";
import '../styles/userInfo.css';


export default function UserInfo() {
  const [userData, setUserData] = useState(null);
  const token = localStorage.getItem("token");
  const email = localStorage.getItem("userEmail");

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/users/get_user/${email}`, {
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

  if (!userData) return <p>Loading user info...</p>;

  return (
    <div className="user-card">
      <h3>👤 {userData.first_name} {userData.last_name}</h3>
      <p><strong>Email:</strong> {userData.email}</p>
      {userData.phone_number && <p><strong>Phone:</strong> {userData.phone_number}</p>}
      {userData.address && <p><strong>Address:</strong> {userData.address}</p>}
    </div>
  );
}
