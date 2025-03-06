import React, { useState, useEffect, useRef } from "react";
import NavbarTeacher from "../components/NavBar/Navbar_teacher";
import { Outlet, useNavigate } from "react-router-dom";
import Cookies from "js-cookie";
import { Link } from "react-router-dom";

export default function TeacherLayout() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = Cookies.get("access_token");
    setIsAuthenticated(!!token);

    const userRole = Cookies.get("role");
    if (!token || userRole !== "TEACHER") {
      navigate("/login");
    }

    // Close dropdown when clicking outside
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleLogout = () => {
    Cookies.remove("access_token");
    window.location.href = "/login";
  };

  return (
    <div className="flex min-h-screen">
      <NavbarTeacher />

      <div className="flex-1 flex flex-col bg-gray-100">
        {/* Top Navbar */}
        <nav className="bg-white shadow-md px-6 py-3 flex justify-between items-center rounded-lg w-full">
          <h1 className="text-lg font-semibold">Smart Attendance System</h1>

          {/* Profile Dropdown */}
          {isAuthenticated && (
            <div className="relative" ref={dropdownRef}>
              <button
                onClick={(e) => {
                  e.stopPropagation(); // Prevent closing when clicking inside
                  setIsDropdownOpen((prev) => !prev);
                }}
                className="text-gray-800 hover:text-gray-600 focus:outline-none px-4 py-2 border rounded-lg"
              >
                My Profile ▼
              </button>

              {/* Dropdown Menu */}
              <div
                className={`absolute right-0 mt-2 w-40 bg-white rounded-lg shadow-lg border border-gray-200 transition-all duration-300 z-50 ${
                  isDropdownOpen
                    ? "opacity-100 scale-100"
                    : "opacity-0 scale-95 pointer-events-none"
                }`}
              >
                <Link
                  to="/profile"
                  className="block px-4 py-2 text-gray-800 hover:bg-gray-200"
                >
                  My Profile
                </Link>
                <button
                  onClick={handleLogout}
                  className="block w-full text-left px-4 py-2 text-gray-800 hover:bg-gray-200"
                >
                  Logout
                </button>
              </div>
            </div>
          )}
        </nav>

        {/* Main Content Area */}
        <div className="flex-1 flex justify-center">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
