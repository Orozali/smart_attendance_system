"use client";
import { motion } from "framer-motion";
import { Carousel } from "react-responsive-carousel";
import "react-responsive-carousel/lib/styles/carousel.min.css";

export default function HomePage() {
  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <div
        className="relative w-full h-[500px] flex items-center justify-center bg-cover bg-center"
        style={{ backgroundImage: "url('/attendance-bg.jpg')" }}
      >
        <div className="absolute inset-0 bg-black bg-opacity-50" />
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="text-white text-center z-10 max-w-2xl"
        >
          <h1 className="text-5xl font-bold mb-4">
            Welcome to Smart Attendance System
          </h1>
          <p className="text-lg mb-6">
            A face recognition-based attendance system for seamless tracking and
            reporting.
          </p>
          <a href="/register">
            <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-300">
              Get Started
            </button>
          </a>
        </motion.div>
      </div>

      <div className="max-w-4xl mx-auto mt-12">
        <Carousel
          autoPlay
          infiniteLoop
          showThumbs={false}
          showStatus={false}
          interval={5000}
          className="rounded-xl shadow-lg"
        >
          <div>
            <img
              src="https://globalcybersecuritynetwork.com/wp-content/uploads/2023/03/face-recognition.jpg"
              alt="Face Recognition"
              className="rounded-lg"
            />
            <p className="legend">AI-Powered Face Recognition</p>
          </div>
          <div>
            <img
              src="https://www.innovatrics.com/wp-content/uploads/2021/10/SmartFace-History-Events_res.jpg.webp"
              alt="Dashboard"
              className="rounded-lg"
            />
            <p className="legend">Real-Time Attendance Reports</p>
          </div>
          <div>
            <img
              src="https://www.lystloc.com/blog/wp-content/uploads/2022/11/blogt.webp"
              alt="Secure Data"
              className="rounded-lg"
            />
            <p className="legend">Secure & Scalable System</p>
          </div>
        </Carousel>
      </div>
    </div>
  );
}
