// src/components/Navbar.jsx
import { Link } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import Cookies from "js-cookie";

export default function Navbar() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const token = Cookies.get("access_token");
    setIsAuthenticated(!!token); // Set true if token exists
    // Close dropdown when clicking outside
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleLogout = () => {
    Cookies.remove("access_token");
    setIsAuthenticated(false);
    window.location.href = "/login"; // Redirect after logout
  };
  return (
    <nav className="bg-gray-800 p-4">
      <div className="flex justify-between items-center">
        {/* Left Side: Home Button */}
        <div>
          <Link
            to="/"
            className="text-white hover:text-gray-400 text-lg font-bold"
          >
            Home
          </Link>
        </div>

        {/* Right Side: Show Profile Dropdown only if authenticated */}
        {isAuthenticated && (
          <div className="relative" ref={dropdownRef}>
            <button
              onClick={toggleDropdown}
              className="text-white hover:text-gray-400 focus:outline-none"
            >
              My Profile ▼
            </button>

            {/* Dropdown Menu */}
            {isOpen && (
              <div className="absolute right-0 mt-2 w-40 bg-white rounded-lg shadow-lg py-2">
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
            )}
          </div>
        )}
      </div>
    </nav>
  );
}
