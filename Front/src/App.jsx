import { Routes, Route, Router } from "react-router-dom";
import HomePage from "./pages/HomePage/HomePage";
import LoginPage from "./pages/Auth/LoginPage";
import RegisterPage from "./pages/Auth/RegisterPage";
import ProtectedRoute from "./pages/Auth/ProtectedRoute";
import Profile from "./pages/Profile";
import Layout from "./pages/Layout";
import StudentLessons from "./pages/Student/Lessons";
import ChooseLesson from "./pages/Student/ChooseLesson";
import Lessons from "./pages/Teacher/Lessons";
import Dashboard from "./pages/Teacher/Dashboard";
import TeacherLayout from "./pages/TeacherLayout";
import LessonInfo from "./pages/Teacher/LessonInfo";
import FaceRecognition from "./pages/FaceRecognition";
import AttendancePage from "./pages/Teacher/AttendancePage";
import AttendanceReport from "./pages/Teacher/AttendanceReport";

function App() {
  return (
    <div>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/face-recognition" element={<FaceRecognition />} />

        {/* Student Layout */}
        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/my-lessons" element={<StudentLessons />} />
            <Route path="/choose-lesson" element={<ChooseLesson />} />
          </Route>
        </Route>

        {/* Teacher Layout */}
        <Route element={<ProtectedRoute />}>
          <Route element={<TeacherLayout />}>
            {/* <Route path="/teacher-home" element={<TeacherHome />} /> */}
            <Route path="/teacher-dashboard" element={<Dashboard />} />
            <Route path="/teacher-lessons" element={<Lessons />} />
            <Route path="/lesson/:lessonId" element={<LessonInfo />} />
            <Route path="/attendance/:lessonId" element={<AttendancePage />} />
            <Route path="/attendance/report" element={<AttendanceReport />} />
          </Route>
        </Route>
      </Routes>

      {/* <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/teacher-home" element={<Dashboard />} />

        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/my-lessons" element={<StudentLessons />} />
            <Route path="/choose-lesson" element={<ChooseLesson />} />
            <Route path="/teacher-lessons" element={<Lessons />} />
          </Route>
        </Route>
      </Routes> */}
    </div>
  );
}

export default App;
