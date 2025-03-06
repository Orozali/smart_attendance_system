import { useEffect, useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function ProfilePage() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      const token = Cookies.get("access_token");
      if (!token) {
        navigate("/login");
        return;
      }
      try {
        const response = await api.get("http://localhost:8000/auth/profile", {
          headers: { Authorization: `Bearer ${token}` },
        });

        setProfile(response.data);
      } catch (err) {
        setError("Failed to fetch profile.");
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [navigate]);

  if (loading) return <p className="text-center mt-10">Loading...</p>;
  if (error) return <p className="text-red-500 text-center mt-10">{error}</p>;
  if (!profile) return null;

  return (
    <div className="flex justify-center items-center bg-gray-100 p-25">
      <div className="w-full max-w-5x gap-6">
        {/* Left Column - Profile Image */}
        <div className=" rounded-lg p-6 flex flex-col items-center">
          <img
            src={
              profile.image ||
              "https://cdn-icons-png.flaticon.com/512/3541/3541871.png"
            }
            alt="Profile"
            className="w-40 h-40 rounded-full  mb-4"
          />
          <h2 className="text-2xl font-bold">
            {profile.name} {profile.surname}
          </h2>
        </div>

        {/* Right Column - Profile Info */}
        <div className="bg-white shadow-md rounded-lg p-6 relative">
          <h1 className="text-3xl font-semibold mb-4 text-center">
            Personal Info
          </h1>
          <span className="h-1/2 w-[1px] absolute top-20 left-1/2 bg-gray-200"></span>
          <div className="flex justify-center items-center gap-10">
            {profile.student_id && (
              <>
                <p className="text-gray-700 text-end w-1/2">
                  <strong>Student Number:</strong>
                </p>

                <p className="w-1/2">{profile.student_id}</p>
              </>
            )}
          </div>
          <div className="flex justify-center items-center gap-10">
            <p className="text-gray-700 text-end w-1/2">
              <strong>Name:</strong>
            </p>
            <p className="w-1/2">{profile.name}</p>
          </div>
          <div className="flex justify-center items-center gap-10">
            <p className="text-gray-700 text-end w-1/2">
              <strong>Surname:</strong>
            </p>
            <p className="w-1/2">{profile.surname}</p>
          </div>
          <div className="flex justify-center items-center gap-10">
            <p className="text-gray-700 text-end w-1/2">
              <strong>Email:</strong>
            </p>
            <p className="w-1/2">{profile.email}</p>
          </div>

          {/* Lessons
          <div className="mt-4 flex justify-center">
            <h3 className="text-lg font-semibold">Lessons:</h3>
            <ul className="list-disc pl-5">
              {profile.lessons.length > 0 ? (
                profile.lessons.map((lesson) => (
                  <li key={lesson.id}>{lesson.name}</li>
                ))
              ) : (
                <p className="text-gray-500">No lessons assigned</p>
              )}
            </ul>
          </div> */}
        </div>
      </div>
    </div>
  );
}
