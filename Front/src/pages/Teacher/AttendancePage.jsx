import { useEffect, useState } from "react";
import Cookies from "js-cookie";
import { useNavigate, useParams } from "react-router-dom";
import api from "../../services/api";
import { toast, ToastContainer } from "react-toastify";

import { BASE_URL } from "../../config";


export default function AttendancePage() {
  const [students, setStudents] = useState([]);
  const [lessonInfo, setLessonInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedDate, setSelectedDate] = useState(null);
  const navigate = useNavigate();
  const { lessonId } = useParams();
  const [timetableId, setTimetableId] = useState(null);
  const [attendanceDates, setAttendanceDates] = useState([]);
  const [day, setDay] = useState(null)
  const [manuallyCheckedIds, setManuallyCheckedIds] = useState([]);

  const showToast = (message, type) => {
    toast(message, {
      position: "top-right",
      autoClose: 1000,
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
  const fetchStudents = async (day) => {
    const token = Cookies.get("access_token");
    if (!token) {
      navigate("/login");
      return;
    }
    try {
      console.log("Fetching students for lessonId:", lessonId, "on day:", day);
      const url = day
        ? `${BASE_URL}/teacher/get-students-from-temporary-db/${lessonId}?day=${day.toISOString().split("T")[0]}`
        : `${BASE_URL}/teacher/get-students-from-temporary-db/${lessonId}`;
  
      const response = await api.get(url, {
        headers: { Authorization: `Bearer ${token}` },
        Accept: 'application/json',
      });
      setStudents(response.data.students);
      setLessonInfo(response.data.lesson_info);
      setTimetableId(response.data.students[0]?.timetable_id);
      
    } catch (err) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Failed to fetch students.");
      }
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAttendanceDates = async () => {
    const token = Cookies.get("access_token");
    if (!token) {
      navigate("/login");
      return;
    }

    try {
      const res = await api.get(`${BASE_URL}/attendance?timetable_id=${timetableId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      console.log(res) 
      setAttendanceDates(res.data);
    } catch (err) {
      console.error("Failed to fetch attendance dates:", err);
    }
  };

  useEffect(() => {
    if (timetableId !== null) {
      console.log("Updated timetableId:", timetableId);
      fetchAttendanceDates();
    }
  }, [timetableId]);
  

  useEffect(() => {
    fetchStudents(selectedDate);
  }, [navigate, selectedDate]);



  const handleDateClick = (dateStr) => {    
    setSelectedDate(new Date(dateStr));
    setLoading(true);
  };


  const handleSave = async () => {
    const token = Cookies.get("access_token");
    if (!token) {
      navigate("/login");
      return;
    }
    const selectedIds = students
    .filter(student => !student.attended)
    .map(student => student.id);

    if (!timetableId) {
      showToast("No students selected or timetable ID missing.", "error")
      return;
    }

    try {
      const dateToUse = selectedDate ?? new Date();
      await api.post(`${BASE_URL}/teacher/attendance/save`, {
        student_ids: selectedIds,
        manually_checked_ids: manuallyCheckedIds,
        timetable_id: timetableId,
        day: dateToUse.toISOString().split("T")[0]
      },
      {
        headers: { Authorization: `Bearer ${token}` },
      });
      showToast("Attendance saved successfully!", "success");
      setTimeout(() => {
        window.location.reload();
      }, 1000000)
    } catch (err) {
      console.error(err);
      showToast(
        err.response?.data?.detail ||
          "Failed to save attendance",
        "error"
      );
    }
  };

  const handleReportClick = () => {    
    navigate('/attendance/report', {
      state: {
        lessonId,
        day: selectedDate ? selectedDate.toISOString().split("T")[0] : null,
      },
    });
  };
  
  

  if (loading) return <p className="text-center mt-10">Loading...</p>;
  if (error) return <p className="text-red-500 text-center mt-10">{error}</p>;

  return (
    <div className="w-full p-6 bg-gray-100">
      <ToastContainer />
      <div>
        <h2 className="text-gray-800 bg-gray-200 border border-gray-200 rounded mb-3">{lessonInfo?.code} {lessonInfo?.name}</h2>
      </div>

      <div className="flex justify-between">
      <div className="flex justify-start gap-5 mb-4">
      {attendanceDates.map((dateStr, index) => (
            <button
              key={dateStr}
              className={`px-4 py-2 rounded ${
                selectedDate?.toISOString().split("T")[0] === dateStr
                  ? "bg-blue-600 text-white"
                  : "bg-green-500 text-white"
              }`}
              onClick={() => handleDateClick(dateStr)}
            >
              {`№ ${index + 1} (${dateStr})`}
            </button>
          ))}
          {/* TODAY BUTTON */}
    
      </div>
  
      <div>
        <button className="bg-blue-500 text-white px-4 py-2 rounded mb-5" onClick={handleReportClick}>Report</button>
      </div>
      </div>
      
      <table className="w-full bg-white rounded-lg">
        <thead>
          <tr>
            <th className="border border-gray-300"  style={{textAlign: 'center'}}>#</th>
            <th className="border border-gray-300 pl-[7px]"  style={{textAlign: 'start'}}>Student ID</th>
            <th className="border border-gray-300 pl-[7px]"  style={{textAlign: 'start'}}>Name</th>
            <th className="border border-gray-300"  style={{textAlign: 'center'}}>Attended</th>
            <th className="border border-gray-300"  style={{textAlign: 'center'}}>Percentage</th>
          </tr>
        </thead>
        <tbody>
          {students
          .sort((a, b) => a.student_id.localeCompare(b.student_id))
          .map((student, index) => (
            <tr key={student.id}>
              <td className="border border-gray-300" style={{textAlign: 'center', paddingTop: '7px'}}>{index + 1}</td>
              <td className="border border-gray-300 pl-[7px]" style={{textAlign: 'start', paddingTop: '7px'}}>{student.student_id}</td>
              <td className="border border-gray-300 pl-[7px]" style={{textAlign: 'start', paddingTop: '7px'}}>{student.name+" "+student.surname}</td>
              <td className="border border-gray-300" style={{textAlign: 'center', paddingTop: '7px'}}>
                <input
                  type="checkbox"
                  checked={student.attended}
                  onChange={() => {
                    const updatedStudents = [...students];
                    updatedStudents[index].attended = !updatedStudents[index].attended;
                    setStudents(updatedStudents);
                    if (updatedStudents[index].attended) {
                      // Add to manuallyCheckedIds if checked
                      setManuallyCheckedIds((prev) => [...new Set([...prev, student.id])]);
                    } else {
                      // Remove from manuallyCheckedIds if unchecked
                      setManuallyCheckedIds((prev) => prev.filter(id => id !== student.id));
                    }
                  }}
                />
              </td>
              <td className={`border border-gray-300 ${student.attendance_percentage >= 25
                        ? "bg-red-200"
                        : student.attendance_percentage >= 18
                        ? "bg-yellow-200"
                        : ""}`} style={{textAlign: 'center', paddingTop: '7px', paddingBottom: '7px'}}>{student.attendance_percentage}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <button
        className="mt-4 bg-blue-500 text-white px-4 py-2 rounded"
        onClick={handleSave}
      >
        Save Attendance
      </button>
    </div>
  );
}
