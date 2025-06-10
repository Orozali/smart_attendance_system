import { Link } from "react-router-dom";
import { useState } from "react";
import {
  Menu,
  Notebook,
  BookCheck,
  CircleUser,
  NotebookPen,
} from "lucide-react";

export default function Navbar() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen h-auto max-h-full">
      <aside
        className={`bg-gray-900 text-white ${
          isSidebarOpen ? "w-64" : "w-20"
        } transition-all duration-300 p-4 flex flex-col h-full`}
      >
        <div className="absolute top-4 left-4">
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="text-white p-2 hover:bg-gray-700 rounded"
          >
            <Menu size={24} />
          </button>
        </div>

        <nav className={`mt-12 space-y-2 ${isSidebarOpen ? "" : "hidden"}`}>
          <Link
            to="/"
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
            to="/my-lessons"
            className="flex items-center space-x-2 px-4 py-2 text-gray-200 hover:bg-gray-700 rounded"
          >
            <Notebook className="w-4 h-4" />
            <span>Courses taken</span>
          </Link>
          
          <Link
            to="/choose-lesson"
            className="flex items-center space-x-2 px-4 py-2 text-gray-200 hover:bg-gray-700 rounded"
          >
            <NotebookPen className="w-4 h-4 text-[#0dcaf0]" />
            <span>Ekle-sil</span>
          </Link>

          <p className="text-sm text-gray-400 font-mono">Other services</p>
          <a
            href="https://eders-bahar2025.manas.edu.kg/my/courses.php"
            target="_blank"
            rel="noopener noreferrer"
            className="block px-4 py-2 text-gray-200 hover:bg-gray-700 rounded"
          >
            E-course
          </a>
          <a
            href="https://elib.manas.edu.kg/index.php"
            target="_blank"
            rel="noopener noreferrer"
            className="block px-4 py-2 text-gray-200 hover:bg-gray-700 rounded"
          >
            E-kitepter
          </a>
        </nav>
      </aside>
    </div>
  );
}
