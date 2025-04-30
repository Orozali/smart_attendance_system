import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import Cookies from "js-cookie";
import api from "../../services/api";
import { CircleChevronLeft } from "lucide-react";

export default function ReportPage() {
  const location = useLocation();
  const { lessonId, day } = location.state || {};
  const [students, setStudents] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = Cookies.get("access_token");
    console.log(day);

    const fetchReportData = async () => {
      if (!token) return;
      try {
        const url = day
        ? `http://localhost:8000/teacher/get-students-from-temporary-db/${lessonId}?day=${day}`
        : `http://localhost:8000/teacher/get-students-from-temporary-db/${lessonId}`;

        console.log(url);
        
        const response = await api.get(
          url,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        console.log(response.data)
        const attendedStudents = response.data.filter(s => s.attended);
  
        // Only update if data actually changed (optional optimization)
        setStudents(prev => {
          const prevIds = prev.map(s => s.id).sort().join(",");
          const newIds = attendedStudents.map(s => s.id).sort().join(",");
          return prevIds !== newIds ? attendedStudents : prev;
        });
      } catch (err) {
        if (err.response?.data?.detail) {
          setError(err.response.data.detail);
        } else {
          setError("Failed to fetch report data.");
        }
      }
    };
  
    // Initial fetch
    if (lessonId) {
      fetchReportData();
      const intervalId = setInterval(fetchReportData, 1000); // 1 second
  
      return () => clearInterval(intervalId); // cleanup on unmount
    }
  }, [lessonId, day]);
  
  if (error) {
    return <p className="text-center text-red-500 mt-10">{error}</p>;
  }

  return (
    <div className="absolute p-6">
      <div className="absolute top-6 left-4"
        onClick={() => window.history.back()}
        >
        <CircleChevronLeft />
      </div>
      <h2 className="text-2xl font-bold text-center mb-6">Attendance Report</h2>

      {students.length === 0 ? (
        <p className="text-center">No students attended.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {students.map((student) => (
            <div
              key={student.id}
              className="flex flex-col items-center bg-white border border-gray-200 rounded-2xl shadow p-4"
            >
              <img
                src={`data:image/jpeg;base64,${student.image}`}
                alt={`${student.name} ${student.surname}`}
                className="w-50 h-50 rounded-[5px] object-cover shadow"
              />
              <div className="mt-4 text-center">
                <h3 className="text-lg font-semibold">
                  {student.name} {student.surname}
                </h3>
                <p className="text-sm text-gray-600">ID: {student.student_id}</p>
                <p className=" text-sm text-gray-800">Entry time: {student.entry_time}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

