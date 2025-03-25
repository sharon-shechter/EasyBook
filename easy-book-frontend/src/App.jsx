// src/App.jsx
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import LogIn from "./pages/LogIn";
import SignUp from "./pages/SignUp";
import UserDashboard from "./pages/UserDashboard";
import ChatWithAgent from "./pages/ChatWithAgent"; 
import BookLesson from "./pages/BookLesson";
import Navbar from "./components/Navbar";
import ManageMyLessons from "./pages/ManageMyLessons";
import About from "./pages/About";
import Contact from "./pages/Contact";
import EditProfile from "./pages/EditProfile";


export default function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<LogIn />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/book" element={<BookLesson />} />
        <Route path="/dashboard" element={<UserDashboard />} />
        <Route path="/chat" element={<ChatWithAgent />} /> 
        <Route path="/my-lessons" element={<ManageMyLessons />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/profile/edit" element={<EditProfile />} />
      </Routes>
    </div>
  );
}
