import { useState } from "react";
import "../styles/bookLesson.css";
import UserInfo from "../components/UserInfo";


export default function BookLesson() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    lesson_date: "",
    lesson_address: "",
    lesson_duration: ""
  });
  const [slots, setSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [extraInfo, setExtraInfo] = useState({
    lesson_type: "",
    lesson_name: "",
    class_number: ""
  });
  const [lessonCreated, setLessonCreated] = useState(null);

  const token = localStorage.getItem("token");

  const handleBasicChange = (e) => {
    const { name, value } = e.target;
    const newValue = name === "lesson_duration" ? Number(value) : value;
    setFormData({ ...formData, [name]: newValue });
  };

  const handleExtraChange = (e) => {
    setExtraInfo({ ...extraInfo, [e.target.name]: e.target.value });
  };

  const fetchSlots = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        lesson_duration: Number(formData.lesson_duration),
      };

      const response = await fetch("http://127.0.0.1:8000/lessons/possible_slots", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error("Failed to fetch slots");

      const data = await response.json();
      setSlots(data);
      setStep(2);
    } catch (err) {
      alert("Error fetching slots: " + err.message);
    }
  };

  const createLesson = async (e) => {
    e.preventDefault();
    const [start, end] = selectedSlot;

    const formatTime = (isoStr) =>
      new Date(isoStr).toTimeString().split(" ")[0]; // "HH:MM:SS"

    const fullLessonData = {
      date: formData.lesson_date,
      start_time: formatTime(start),
      end_time: formatTime(end),
      lesson_type: extraInfo.lesson_type,
      lesson_name: extraInfo.lesson_name,
      class_number: Number(extraInfo.class_number), // Must be int
      duration: formData.lesson_duration,
      lesson_adress: formData.lesson_address, // Match backend field
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/lessons/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(fullLessonData),
      });

      if (!response.ok) throw new Error("Failed to create lesson");

      const createdLesson = await response.json();
      setLessonCreated(createdLesson);
      setStep(4);
    } catch (err) {
      alert("Error creating lesson: " + err.message);
    }
  };

  return (
    <>
      <div className="book-lesson-container">
        <h2>📘 Book a New Lesson</h2>
  
        {step === 1 && (
          <form onSubmit={fetchSlots} className="lesson-form">
            <input
              type="date"
              name="lesson_date"
              onChange={handleBasicChange}
              required
            />
            <input
              type="text"
              name="lesson_address"
              placeholder="Lesson Address - full address (city, street, number)"
              onChange={handleBasicChange}
              required
            />
            <input
              type="number"
              name="lesson_duration"
              placeholder="Duration (in minutes)"
              onChange={handleBasicChange}
              required
            />
            <button type="submit">Find Time Slots</button>
          </form>
        )}
  
        {step === 2 && (
          <div>
            <h3>🕓 Available Time Slots:</h3>
            {slots.length === 0 ? (
              <p>No available time slots for this date.</p>
            ) : (
              <form onSubmit={() => setStep(3)}>
                {slots.map((slot, index) => (
                  <label key={index} className="slot-option">
                    <input
                      type="radio"
                      name="slot"
                      value={slot}
                      onChange={() => setSelectedSlot(slot)}
                      required
                    />
                    {new Date(slot[0]).toLocaleTimeString()} -{" "}
                    {new Date(slot[1]).toLocaleTimeString()}
                  </label>
                ))}
                <button type="submit" disabled={!selectedSlot}>
                  Continue
                </button>
              </form>
            )}
          </div>
        )}
  
        {step === 3 && (
          <form onSubmit={createLesson} className="lesson-form">
            <h3>📋 Add Lesson Details</h3>
            <input
              type="text"
              name="lesson_type"
              placeholder="Home or Zoom"
              onChange={handleExtraChange}
              required
            />
            <input
              type="text"
              name="lesson_name"
              placeholder="Lesson Name (like Math or English)"
              onChange={handleExtraChange}
              required
            />
            <input
              type="text"
              name="class_number"
              placeholder="Class"
              onChange={handleExtraChange}
              required
            />
            <button type="submit">Create Lesson</button>
          </form>
        )}
  
        {step === 4 && lessonCreated && (
          <div className="lesson-summary">
            <h3>✅ Lesson Created Successfully!</h3>
            <p>
              <strong>{lessonCreated.lesson_name}</strong> on{" "}
              {lessonCreated.date}
            </p>
            <p>
              {lessonCreated.start_time} - {lessonCreated.end_time}
            </p>
            <p>Address: {lessonCreated.lesson_adress}</p>
            <p>Type: {lessonCreated.lesson_type}</p>
          </div>
        )}
      </div>
  
      <UserInfo />
    </>
  );
  
}
