import { useState, useEffect } from "react";
import axios from "axios";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Cookies from "js-cookie";
import api from "../../services/api";

import { BASE_URL } from "../../config";

export default function ChooseLesson() {
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectMode, setSelectMode] = useState(false);
  const [selectedLessons, setSelectedLessons] = useState([]);

  const showToast = (message, type) => {
    toast(message, {
      position: "top-right",
      autoClose: 5000,
      hideProgressBar: true,
      closeOnClick: true,
      pauseOnHover: false,
      draggable: true,
      style: {
        backgroundColor: type === "success" ? "green" : "red",
        color: "white",
        fontWeight: "bold",
      },
    });
  };
  useEffect(() => {
    const fetchLessons = async () => {
      const token = Cookies.get("access_token");
      if (!token) {
        navigate("/login");
        return;
      }
      try {
        const response = await axios.get(`${BASE_URL}/lesson/all`,
          {
            headers: {
              "ngrok-skip-browser-warning": "69420"
            },
          }
        );
        setLessons(response.data);
      } catch (err) {
        setError("Failed to load lessons. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchLessons();
  }, []);

  const toggleLesson = (id) => {
    setSelectedLessons((prev) =>
      prev.includes(id)
        ? prev.filter((lessonId) => lessonId !== id)
        : [...prev, id]
    );
  };

  const handleSave = async () => {
    const token = Cookies.get("access_token");
    if (!token) {
      navigate("/login");
      return;
    }
    if (selectedLessons.length === 0) {
      showToast("Please select at least one lesson!", "error");
      return;
    }

    try {
      const response = await api.post(
        `${BASE_URL}/student/choose-lesson`,
        selectedLessons,
        {
          headers: {
             Authorization: `Bearer ${token}`,
            "ngrok-skip-browser-warning": "69420"
          },
        }
      );
      if (response.status === 200) {
        showToast(
          response.data.message || "Lessons selected successfully!",
          "success"
        );
        setSelectMode(false);
        setSelectedLessons([]);
      }
    } catch (err) {
      console.error("Error:", err.response?.data);
      showToast(err.response?.data?.detail || "Something went wrong!", "error");
    }
  };

  return (
    <div className="min-h-screen p-6 bg-gray-100">
      <ToastContainer />
      <div className="bg-white shadow-lg rounded-lg p-6">
        <div className="flex justify-between mb-4">
          <h1 className="text-xl font-semibold">Алган сабактары</h1>
          <button
            onClick={() => setSelectMode(!selectMode)}
            className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition"
          >
            {selectMode ? "Cancel" : "Choose Lesson"}
          </button>
        </div>

        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p className="text-red-500">{error}</p>
        ) : (
          <table className="w-full border-collapse border border-gray-200">
            <thead>
              <tr className="bg-gray-100">
                <th className="border border-gray-200 p-2">
                  {selectMode ? "Select" : "#"}
                </th>
                <th className="border border-gray-200 p-2">Code</th>
                <th className="border border-gray-200 p-2">Lesson Name</th>
                <th className="border border-gray-200 p-2">Teacher</th>
              </tr>
            </thead>
            <tbody>
              {lessons.map((lesson, index) => (
                <tr key={lesson.id} className="border hover:bg-gray-50">
                  <td className="border border-gray-200 p-2 text-center">
                    {selectMode ? (
                      <input
                        type="checkbox"
                        checked={selectedLessons.includes(lesson.id)}
                        onChange={() => toggleLesson(lesson.id)}
                        className="w-5 h-5 text-blue-600"
                      />
                    ) : (
                      index + 1
                    )}
                  </td>
                  <td className="border border-gray-200 p-2 text-center">
                    {lesson.code}
                  </td>
                  <td className="border border-gray-200 p-2">{lesson.name}</td>
                  <td className="border border-gray-200 p-2 text-center">
                    {lesson.teacher?.name} {lesson.teacher?.surname}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {selectMode && (
          <div className="mt-4 flex justify-end">
            <button
              onClick={handleSave}
              className="bg-[#32ba62] text-white px-6 py-2 rounded-md hover:bg-green-600 transition"
            >
              Save
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
