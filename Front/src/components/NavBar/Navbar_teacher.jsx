import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Cookies from "js-cookie";
import axios from "axios";
import {
  Menu,
  NotepadText,
  BookCheck,
  CircleUser,
  NotebookPen,
  SquareLibrary,
  ChevronRight,
  ChevronDown,
} from "lucide-react";
import api from "../../services/api";

export default function Navbar_teacher() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [lessons, setLessons] = useState([]);
  const [isLessonsOpen, setIsLessonsOpen] = useState(false);
  const navigate = useNavigate();

  // Fetch lessons from the API
  useEffect(() => {
    const accessToken = Cookies.get("access_token");
    if (!accessToken) {
      setError("Access token is missing");
      setLoading(false);
      return;
    }
    api
      .get("http://localhost:8000/teacher/get-lessons", {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        setLessons(response.data); // Assuming the response is an array of lessons
      })
      .catch((error) => {
        console.error("Error fetching lessons:", error);
      });
  }, []); // Empty dependency array means this runs once on component mount

  const handleLessonClick = (lessonId) => {
    // Navigate to the lesson details page, assuming the path includes lesson ID
    navigate(`/lesson/${lessonId}`);
  };

  return (
    <div className="flex">
      {/* Sidebar */}
      <aside
        className={`bg-gray-900 text-white ${
          isSidebarOpen ? "w-74" : "w-20"
        } transition-all duration-300 p-4 flex flex-col h-full`}
      >
        {/* Sidebar Toggle Button - Always Fixed at Top */}
        <div className="absolute top-4 left-4">
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="text-white p-2 hover:bg-gray-700 rounded"
          >
            <Menu size={24} />
          </button>
        </div>

        {/* Sidebar Links */}
        <nav className={`mt-12 space-y-2 ${isSidebarOpen ? "" : "hidden"}`}>
          <Link
            to="/teacher-dashboard"
            className="flex items-center space-x-2 px-2 py-2 text-gray-200 hover:bg-gray-700 rounded"
          >
            <img
              className="w-6 h-6"
              src="https://obistest.manas.edu.kg/images/logo.png"
              alt=""
            />
            <span>OBIS</span>
          </Link>

          <p className="text-sm text-gray-400 font-mono">Personal Data</p>
          <Link
            to="/profile"
            className="flex items-center space-x-2 px-2 py-2 text-gray-200 hover:bg-gray-700 rounded"
          >
            <CircleUser className="w-4 h-4" />
            <span> Personal Info</span>
          </Link>
          <p className="text-sm text-gray-400 font-mono">Course Info</p>
          <div
            className="flex items-center justify-between space-x-2 px-2 py-2 text-gray-200 hover:bg-gray-700 rounded cursor-pointer"
            onClick={() => setIsLessonsOpen(!isLessonsOpen)}
          >
            <div className="flex items-center space-x-2">
              <SquareLibrary className="w-4 h-4" />
              <span>My Lessons</span>
            </div>
            {/* Arrow Icon */}
            {isLessonsOpen ? (
              <ChevronDown className="w-4 h-4 text-gray-400" />
            ) : (
              <ChevronRight className="w-4 h-4 text-gray-400" />
            )}
          </div>

          {/* Render List of Lessons if My Lessons is clicked */}
          {isLessonsOpen && (
            <div className="mt-2 space-y-1">
              {lessons.length > 0 ? (
                lessons.map((lesson) => (
                  <div
                    key={lesson.id}
                    onClick={() => handleLessonClick(lesson.id)}
                    className="flex items-center text-gray-100 px-4 py-2 hover:bg-gray-700 rounded cursor-pointer"
                  >
                    <NotepadText className="h-4 w-4 text-gray-400 mr-1.5" />
                    <div className="flex items-center gap-x-2 whitespace-nowrap">
                      <span className="text-xs text-gray-400">
                        {lesson.code}
                      </span>
                      <span className="text-xs text-gray-400">
                        {lesson.name}
                      </span>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-gray-400 px-4 py-2">No lessons available</p>
              )}
            </div>
          )}
        </nav>
      </aside>
    </div>
  );
}
