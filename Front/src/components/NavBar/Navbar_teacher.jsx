import { Link } from "react-router-dom";
import { useState } from "react";
import {
  Menu,
  Notebook,
  BookCheck,
  CircleUser,
  NotebookPen,
} from "lucide-react";

export default function Navbar_teacher() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="flex">
      {/* Sidebar */}
      <aside
        className={`bg-gray-900 text-white ${
          isSidebarOpen ? "w-64" : "w-20"
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
            className="flex items-center space-x-2 px-4 py-2 text-gray-200 hover:bg-gray-700 rounded"
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
            className="flex items-center space-x-2 px-4 py-2 text-gray-200 hover:bg-gray-700 rounded"
          >
            <CircleUser className="w-4 h-4" />
            <span> Personal Info</span>
          </Link>
          <p className="text-sm text-gray-400 font-mono">Course Info</p>
          <Link
            to="/teacher-lessons"
            className="flex items-center space-x-2 px-4 py-2 text-gray-200 hover:bg-gray-700 rounded"
          >
            <Notebook className="w-4 h-4" />
            <span>My Lessons</span>
          </Link>
        </nav>
      </aside>
    </div>
  );
}
