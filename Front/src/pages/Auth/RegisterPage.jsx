import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function RegisterPage() {
  const [capturing, setCapturing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    surname: "",
    email: "",
    studentNumber: "",
    password: "",
    images: [],
  });
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const navigate = useNavigate();
  const [errors, setErrors] = useState({});
  const [faceDetected, setFaceDetected] = useState(false);
  const [feedbackMessage, setFeedbackMessage] = useState(
    "Please position your face within the circle"
  );

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const showToast = (message, type) => {
    toast(message, {
      position: "top-right",
      autoClose: 8000,
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

  const startCapture = async () => {
    setCapturing(true);
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoRef.current.srcObject = stream;
    videoRef.current.play();
    captureImages();
  };

  const captureImages = async () => {
    let images = [];
    for (let i = 0; i < 100; i++) {
      await new Promise((resolve) => setTimeout(resolve, 100)); // Delay to simulate real-time capture
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
      images.push(canvas.toDataURL("image/jpeg"));
    }
    setFormData((prev) => ({ ...prev, images })); // Preserve other form fields
    setCapturing(false);
    videoRef.current.srcObject.getTracks().forEach((track) => track.stop());
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const newErrors = {};
    if (!formData.name.trim()) newErrors.name = "Введите имя";
    if (!formData.surname.trim()) newErrors.surname = "Введите фамилию";
    if (!formData.email.trim()) {
      newErrors.email = "Введите email";
    } else if (!/^\S+@\S+\.\S+$/.test(formData.email)) {
      newErrors.email = "Некорректный email";
    }
    if (!formData.studentNumber.trim()) newErrors.studentNumber = "Введите ID";
    if (!formData.password.trim()) {
      newErrors.password = "Введите пароль";
    } else if (formData.password.length < 6) {
      newErrors.password = "Пароль должен содержать минимум 6 символов";
    }
    if (formData.images.length < 100) {
      newErrors.images = "Зарегистрируйте свое лицо";
    }

    // If there are errors, stop submission and update state
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    } else {
      setErrors({}); // Clear errors if form is valid
    }

    setLoading(true);

    // Prepare FormData
    const formDataToSend = new FormData();
    formDataToSend.append("name", formData.name);
    formDataToSend.append("surname", formData.surname);
    formDataToSend.append("email", formData.email);
    formDataToSend.append("password", formData.password);
    formDataToSend.append("student_id", formData.studentNumber);

    // Convert each image to a Blob and append to FormData
    formData.images.forEach((image, index) => {
      const byteString = atob(image.split(",")[1]);
      const arrayBuffer = new ArrayBuffer(byteString.length);
      const uintArray = new Uint8Array(arrayBuffer);
      for (let i = 0; i < byteString.length; i++) {
        uintArray[i] = byteString.charCodeAt(i);
      }
      const blob = new Blob([uintArray], { type: "image/jpeg" });
      formDataToSend.append("files", blob, `image_${index + 1}.jpg`);
    });

    try {
      const response = await axios.post(
        // "http://127.0.0.1:8000/auth/register",
        "https://40c8-178-217-174-2.ngrok-free.app/auth/register",
        formDataToSend,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      setLoading(false);
      showToast("Registration successful!", "success");
      setTimeout(() => {
        navigate("/");
      }, 3000);
    } catch (error) {
      setLoading(false);
      showToast(
        error.response?.data?.detail ||
          "Registration failed. Please try again.",
        "error"
      );
    }
  };

  const detectFace = () => {
    // You can integrate face detection logic here
    const video = videoRef.current;
    // Simple face detection logic using canvas or libraries like face-api.js

    // Example: Update face detection status (for now it's just a mock)
    if (video) {
      const rect = video.getBoundingClientRect();
      if (rect.width < 100 || rect.height < 100) {
        setFaceDetected(false);
        setFeedbackMessage("Please move closer to the camera.");
      } else {
        setFaceDetected(true);
        setFeedbackMessage("Face detected! Please wait...");
      }
    }
  };

  useEffect(() => {
    if (capturing) {
      const intervalId = setInterval(detectFace, 500);
      return () => clearInterval(intervalId);
    }
  }, [capturing]);

  return (
    <div className="min-h-screen flex flex-col items-center pt-12 bg-gray-100">
      <ToastContainer />
      <h1 className="text-4xl font-semibold mb-4">Register</h1>
      {!capturing ? (
        <form
          onSubmit={handleSubmit}
          className="w-full max-w-sm bg-white p-6 rounded-lg shadow-lg"
        >
          {["name", "surname", "email", "studentNumber", "password"].map(
            (field, idx) => (
              <div className="mb-4" key={idx}>
                <label className="block text-gray-700">
                  {field.charAt(0).toUpperCase() + field.slice(1)}
                </label>
                <input
                  type={field === "password" ? "password" : "text"}
                  name={field}
                  className="w-full p-2 mt-2 border border-gray-300 rounded-md"
                  placeholder={`Enter your ${field}`}
                  onChange={handleInputChange}
                  value={formData[field]}
                  disabled={loading}
                />
                {errors[field] && (
                  <p className="text-red-500 text-sm mt-1">{errors[field]}</p>
                )}
              </div>
            )
          )}

          <button
            type="button"
            onClick={startCapture}
            className={`w-full py-2 mb-2 rounded-md flex items-center justify-center ${
              formData.images.length >= 100
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-green-600 hover:bg-green-500"
            } text-white`}
            disabled={formData.images.length >= 100}
          >
            {formData.images.length >= 100 ? (
              <>✅ Face Registered</>
            ) : (
              "Register your face"
            )}
          </button>
          {errors.images && (
            <p className="text-red-500 text-sm mt-1">{errors.images}</p>
          )}
          <button
            type="submit"
            className={`w-full py-2 rounded-md ${
              loading ? "bg-gray-400" : "bg-blue-600"
            } text-white hover:${loading ? "" : "bg-blue-500"}`}
            disabled={loading}
          >
            {loading ? (
              <div className="flex justify-center items-center">
                <div className="animate-spin rounded-full border-t-4 border-white w-6 h-6 mr-2"></div>
                Signing up...
              </div>
            ) : (
              "Sign up"
            )}
          </button>
        </form>
      ) : (
        <div className="flex flex-col items-center relative">
          <video
            ref={videoRef}
            className="w-85 h-85 rounded-full border-4 border-gray-600"
            autoPlay
          />
          <canvas ref={canvasRef} width="640" height="480" hidden />
          <div className="absolute bottom-1 text-white text-lg font-semibold bg-black bg-opacity-50 p-1 rounded">
            {feedbackMessage}
          </div>
        </div>
      )}
    </div>
  );
}
