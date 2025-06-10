import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Cookies from "js-cookie";
import { Eye, EyeOff } from "lucide-react";

import { BASE_URL } from "../../config";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const [showPass, setShowPass] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const show = () => {
    setShowPass(!showPass);
  };

  const login = async (e) => {
    e.preventDefault();

    const newErrors = {};
    if (!username.trim()) newErrors.username = "Введите ID";
    if (!password.trim()) newErrors.password = "Введите пароль";

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    setErrors({});
    try {
      const response = await axios.post(
        `${BASE_URL}/auth/login`,
        { username: username, password: password },
        {
          headers: { "Content-Type": "application/json", "ngrok-skip-browser-warning": "69420"},
        }
      );
      const role = response.data.role;
      saveTokenToCookies(
        response.data.access_token,
        response.data.refresh_token,
        response.data.role
      );
      if (role == "TEACHER") {
        setLoading(false);
        navigate("/teacher-dashboard");
      } else {
        setLoading(false);
        navigate("/");
      }
    } catch (error) {
      setLoading(false);
      alert(
        error.response?.data?.detail || "Registration failed. Please try again."
      );
    }
  };

  const saveTokenToCookies = (access_token, refresh_token, role) => {
    const inFiveHours = new Date(new Date().getTime() + 5 * 60 * 60 * 1000);
    Cookies.set("access_token", access_token, {
      expires: inFiveHours,
      secure: true,
      sameSite: "Strict",
    });

    Cookies.set("refresh_token", refresh_token, {
      secure: true,
      expires: inFiveHours,
      sameSite: "Strict",
    });

    Cookies.set("role", role);
  };

  return (
    <div className="min-h-screen flex flex-col items-center pt-12 bg-gray-100">
      <h1 className="text-4xl font-semibold mb-4">Sign In</h1>

      <form
        className="w-full max-w-sm bg-white p-6 rounded-lg shadow-lg"
        onSubmit={login}
      >
        <div className="mb-4">
          <label className="block text-gray-700">Email</label>
          <input
            type="text"
            className="w-full p-2 mt-2 border border-gray-300 rounded-md"
            placeholder="Enter your student ID"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            disabled={loading}
          />
          {errors.username && (
            <p className="text-red-500 text-sm mt-1">{errors.username}</p>
          )}
        </div>

        <div className="mb-4">
          <label className="block text-gray-700">Password</label>
          <div className="relative">
            <input
              type={showPass ? "text" : "password"}
              className="w-full p-2 mt-2 border border-gray-300 rounded-md relative"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
            />
            <span
              onClick={show}
              className="absolute right-2 top-1/2 -translate-y-1/3 cursor-pointer"
            >
              {!showPass ? (
                <Eye className="size-5" />
              ) : (
                <EyeOff className="size-5" />
              )}
            </span>
            {errors.password && (
              <p className="text-red-500 text-sm mt-1">{errors.password}</p>
            )}
          </div>
        </div>

        <button
          type="submit"
          className={`w-full py-2 bg-blue-600 text-white rounded-md hover:bg-blue-500 ${
            loading ? "bg-gray-400" : ""
          }`}
          disabled={loading}
        >
          {loading ? (
            <div className="flex justify-center items-center">
              <div className="animate-spin rounded-full border-t-4 border-white w-6 h-6 mr-2"></div>
              Logging in...
            </div>
          ) : (
            "Sign In"
          )}
        </button>

        <div className="mt-4">
          <p className="text-gray-600">
            If you don't have an account,{" "}
            <a href="/register" className="text-blue-600 hover:text-blue-500">
              please sign up!
            </a>
          </p>
        </div>
      </form>
    </div>
  );
}
