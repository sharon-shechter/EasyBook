import { useEffect, useState } from "react";
import UserInfo from "../components/UserInfo";
import "../styles/manageMyLessons.css";

export default function ManageMyLessons() {
  const [lessons, setLessons] = useState([]);
  const token = localStorage.getItem("token");
  const apiUrl = import.meta.env.VITE_API_URL;

  useEffect(() => {
    const fetchLessons = async () => {
      try {
        const res = await fetch(`${apiUrl}/lessons/get_lessons`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!res.ok) throw new Error("Failed to fetch lessons");

        const data = await res.json();
        setLessons(data);
      } catch (err) {
        console.error("Failed to fetch lessons:", err);
      }
    };

    fetchLessons();
}, [token, apiUrl]); 

  const handleDelete = async (lesson_id) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this lesson?");
    if (!confirmDelete) return;

    try {
      const res = await fetch(`${apiUrl}/lessons/delete/${lesson_id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) throw new Error("Failed to delete lesson");

      alert("Lesson deleted successfully!");

      const updatedLessons = lessons.filter((l) => l.lesson_id !== lesson_id);
      setLessons(updatedLessons);
    } catch (err) {
      alert("Error deleting lesson: " + err.message);
    }
  };

  return (
    <div className="manage-lessons-page">
      <h2>📚 Manage My Lessons</h2>

      <UserInfo />

      <h3>🗓️ Upcoming Lessons</h3>

      {lessons.length === 0 ? (
        <p>No lessons found.</p>
      ) : (
        <div className="lesson-list">
          {lessons.map((lesson) => (
            <div key={lesson.lesson_id} className="lesson-card">
              <h4>{lesson.lesson_name} ({lesson.lesson_type})</h4>
              <p>Date: {lesson.date}</p>
              <p>Time: {lesson.start_time} - {lesson.end_time}</p>
              <p>Address: {lesson.lesson_adress}</p>
              <p>Class: {lesson.class_number}</p>
              <button onClick={() => handleDelete(lesson.lesson_id)}>🗑️ Delete</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
