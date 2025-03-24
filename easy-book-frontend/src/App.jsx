// src/App.jsx
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import LogIn from "./pages/LogIn";
import SignUp from "./pages/SignUp";
import ManageLessons from "./pages/ManageLessons";
import ChatWithAgent from "./pages/ChatWithAgent"; 
import BookLesson from "./pages/BookLesson";
import Navbar from "./components/Navbar";

export default function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<LogIn />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/book" element={<BookLesson />} />
        <Route path="/lessons" element={<ManageLessons />} />
        <Route path="/chat" element={<ChatWithAgent />} /> 
      </Routes>
    </div>
  );
}
