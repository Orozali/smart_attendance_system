import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../../services/api";
import Cookies from "js-cookie";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function LessonInfo() {
  const { lessonId } = useParams();
  const [lesson, setLesson] = useState(null);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [loadingStudents, setLoadingStudents] = useState(false);
  const [studentsError, setStudentsError] = useState(null);
  const [showStudents, setShowStudents] = useState(false);

  useEffect(() => {
    const accessToken = Cookies.get("access_token");
    if (!accessToken) {
      setError("Access token is missing");
      setLoading(false);
      return;
    }

    const parsedId = parseInt(lessonId, 10);
    if (isNaN(parsedId)) {
      setError("Invalid lesson ID");
      setLoading(false);
      return;
    }

    api
      .get(`http://localhost:8000/teacher/get-lesson/${parsedId}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        setLesson(response.data);
      })
      .catch(() => {
        setError("Failed to fetch lesson info");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [lessonId]);

  const fetchStudents = async () => {
    setLoadingStudents(true);
    setStudentsError(null);

    try {
      const parsedId = parseInt(lessonId, 10);
      if (isNaN(parsedId)) {
        setError("Invalid lesson ID");
        setLoading(false);
        return;
      }
      const response = await api.get(
        `http://localhost:8000/teacher/get-students/${parsedId}`,
        {
          headers: {
            Authorization: `Bearer ${Cookies.get("access_token")}`,
          },
        }
      );
      setStudents(response.data);
    } catch (err) {
      setStudentsError("Failed to load students. Please try again.");
    } finally {
      setLoadingStudents(false);
    }
  };

  const handleShowStudents = () => {
    if (!showStudents) {
      fetchStudents();
    }
    setShowStudents(!showStudents);
  };

  return (
    <div className="min-h-screen p-6 bg-gray-100 flex justify-center">
      <ToastContainer />
      <div className="bg-white shadow-lg rounded-lg p-6 w-full max-w-screen-xl">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-xl font-semibold">Lesson Information</h1>
          <div className="flex space-x-2">
          {loading ? (
          <p className="text-center text-gray-500">Loading...</p>
        ) : error ? (
          <p className="text-center text-red-500">{error}</p>
        ) : lesson ? (
          <Link
            to={`/attendance/${lesson.id}`}
            className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition"
          >
            <span>Жоктомо</span>
          </Link>
        ) : null}
          </div>
        </div>

        {loading || error ? null :(
          <table className="w-full border border-gray-300">
            <thead className="bg-gray-100">
              <tr>
                <th className="border border-gray-300 p-2">#</th>
                <th className="border border-gray-300 p-2">
                  Академиялык бирими
                </th>
                <th className="border border-gray-300 p-2">Сабактын коду</th>
                <th className="border border-gray-300 p-2">Семестр</th>
                <th className="border border-gray-300 p-2">Студенттин саны</th>
                <th className="border border-gray-300 p-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border hover:bg-gray-50">
                <td className="border border-gray-300 p-2 text-center">1</td>
                <td className="border border-gray-300 p-2">
                  Инженердик факультет
                  <br />
                  Программалык инженерия
                  <br />
                  Программалык инженерия
                </td>
                <td className="border border-gray-300 p-2 text-center">
                  {lesson.code}
                </td>
                <td className="border border-gray-300 p-2 text-center">
                  4. Семестр
                </td>
                <td className="border border-gray-300 p-2 text-center">
                  {lesson.countOfStudent}
                </td>
                <td className="border border-gray-300 p-2 space-y-2">
                  <button className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition">
                    Көчүрүп алуу
                  </button>
                  <button className="bg-gray-500 text-white px-3 py-1 rounded hover:bg-gray-600 transition">
                    Группанын тизмеси
                  </button>
                  <button className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600 transition">
                    Сынак отчёту жана катышуу тизмеси
                  </button>
                  <button className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition">
                    Жоктомо тизмеси
                  </button>
                  <button className="bg-indigo-500 text-white px-3 py-1 rounded hover:bg-indigo-600 transition">
                    Сабакка катышуу боюнча отчет
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        )}

        {/* Toggle Student List */}
        <div className="flex space-x-2 mt-4">
          <button
            onClick={handleShowStudents}
            className="bg-blue-500 text-white px-4 py-1 rounded-md hover:bg-blue-600 transition"
          >
            {showStudents ? "Жашыруу" : "Студенттердин тизмеси"}
          </button>
        </div>

        {/* Student List */}
        {showStudents && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <h2 className="text-lg font-semibold mb-2">Студенттер</h2>

            {loadingStudents ? (
              <p className="text-gray-500">Жүктөлүүдө...</p>
            ) : studentsError ? (
              <p className="text-red-500">{studentsError}</p>
            ) : (
              <table className="w-full border border-gray-300">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="border border-gray-300 p-2">
                      Студенттик ID
                    </th>
                    <th className="border border-gray-300 p-2">Аты</th>
                    <th className="border border-gray-300 p-2">Фамилиясы</th>
                  </tr>
                </thead>
                <tbody>
                  {students.length > 0 ? (
                    students.map((student, index) => (
                      <tr key={student.id} className="border hover:bg-gray-50">
                        <td className="border border-gray-300 p-2 text-center">
                          {student.student_id}
                        </td>
                        <td className="border border-gray-300 p-2">
                          {student.name}
                        </td>
                        <td className="border border-gray-300 p-2">
                          {student.surname}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td
                        colSpan="3"
                        className="border p-2 text-center text-gray-500"
                      >
                        Студенттер жок
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
