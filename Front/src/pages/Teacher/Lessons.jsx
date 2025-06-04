import { useEffect, useState } from "react";
import Cookies from "js-cookie";
import api from "../../services/api";
import { BASE_URL } from "../../config";

export default function StudentLessons() {
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLessons = async () => {
      const accessToken = Cookies.get("access_token");
      if (!accessToken) {
        setError("Access token is missing");
        setLoading(false);
        return;
      }

      try {
        const response = await api.get(
          `${BASE_URL}/teacher/get-lessons`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              "Content-Type": "application/json",
              "ngrok-skip-browser-warning": "69420"
            },
          }
        );

        setLessons(response.data);
      } catch (err) {
        setError("Failed to fetch lessons");
      } finally {
        setLoading(false);
      }
    };

    fetchLessons();
  }, []);

  return (
    <div className="min-h-screen p-6 bg-gray-100">
      <div className="bg-white shadow-lg rounded-lg p-6">
        <h1 className="text-xl font-semibold mb-4">My lessons</h1>
        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p className="text-red-500">{error}</p>
        ) : (
          <table className="w-full border-collapse border border-gray-200">
            <thead>
              <tr className="bg-gray-100">
                <th className="border border-gray-200 p-2">#</th>
                <th className="border border-gray-200 p-2">Code</th>
                <th className="border border-gray-200 p-2">Name</th>
              </tr>
            </thead>
            <tbody>
              {lessons.map((lesson, index) => (
                <tr key={lesson.id} className="border">
                  <td className="border border-gray-200 p-2 text-center">
                    {index + 1}
                  </td>
                  <td className="border border-gray-200 p-2">{lesson.code}</td>
                  <td className="border border-gray-200 p-2">{lesson.name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
