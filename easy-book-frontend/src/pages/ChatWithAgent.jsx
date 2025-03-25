import { useState } from "react";
import "../styles/chat.css"; 
import UserInfo from "../components/UserInfo";


export default function ChatWithAgent() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const user_id = localStorage.getItem("userId");
    const newMessage = { role: "user", content: input };

    setMessages((prev) => [...prev, newMessage]);
    setInput("");

    try {
      const response = await fetch("http://127.0.0.1:8000/agent/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: user_id,
          content: input,
        }),
      });

      const data = await response.json();
      const reply = data.response;
      setMessages((prev) => [...prev, { role: "agent", content: reply }]);
    } catch (err) {
      console.error("Chat error:", err);
      setMessages((prev) => [
        ...prev,
        { role: "agent", content: "❌ Error talking to agent." },
      ]);
    }
  };

  return (
    <>
      <div className="chat-container">
        <h1>Bob</h1>
        <div className="chat-box">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-message ${msg.role === "user" ? "user" : "agent"}`}
            >
              {msg.content}
            </div>
          ))}
        </div>
        <form className="chat-input" onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask something..."
          />
          <button type="submit">Send</button>
        </form>
      </div>
  
      <UserInfo />
    </>
  );
}
