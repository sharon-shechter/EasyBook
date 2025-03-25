import "../styles/contact.css";

export default function Contact() {
  return (
    <div className="contact-container">
      <h1>Contact Me</h1>
      <p>If you have questions or just want to say hi — feel free to reach out! 😊</p>

      <div className="contact-info">
        <div className="contact-item">
          <span>📧</span>
          <p href="mail">Sharonshechter1@gmail.com</p>
        </div>

        <div className="contact-item">
          <span>📞</span>
          <p href="tel">+972-547633704</p>
        </div>

        <div className="contact-item">
          <span>📍</span>
          <p>Based in Tel Aviv, Israel</p>
        </div>
      </div>
    </div>
  );
}
