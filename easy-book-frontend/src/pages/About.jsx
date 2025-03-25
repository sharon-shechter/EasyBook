import "../styles/about.css";

export default function About() {
  return (
    <div className="about-container">
      <h1>About Easy Book</h1>
      <p>
        Hi! I'm Sharon Shechter, a passionate computer science student and private tutor based in Tel Aviv.
        I built Easy Book to simplify how students book lessons with me, and to make scheduling clear, fast, and reliable.
      </p>
      <p>
        With years of tutoring experience in math and computer science, I’ve helped over 30 students succeed
        — from high schoolers to university students.
      </p>
      
      <p>
        Whether you're booking a lesson, checking availability, or just exploring — I'm glad you're here. 🙌
      </p>

      <div className="lessons-section">
    <h2>My Lessons</h2>
    <div className="circle-lessons">
        <div className="circle-card">
        <h3>📍 In-Person</h3>
        <p>₪150/hour</p>
        <span className="circle-desc">At student's home</span>
        </div>
        <div className="circle-card">
        <h3>💻 Zoom</h3>
        <p>₪120/hour</p>
        <span className="circle-desc">Online via Zoom</span>
        </div>
    </div>
    </div>

      <p className="signature">– Sharon</p>
    </div>
  );
}
