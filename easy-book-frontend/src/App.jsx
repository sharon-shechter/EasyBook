// src/App.jsx
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import SignIn from "./pages/LogIn";
import SignUp from "./pages/SignUp";
import ManageLessons from "./pages/ManageLessons";
import Navbar from "./components/Navbar";
import LogIn from "./pages/LogIn";

export default function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<LogIn />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/lessons" element={<ManageLessons />} />
      </Routes>
    </div>
  );
}