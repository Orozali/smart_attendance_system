import React, { useEffect, useRef, useState } from "react";

const FaceRecognition = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const ws = useRef(null);
  const [faces, setFaces] = useState([]);

  useEffect(() => {
    // Start WebRTC Camera
    navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }

      // Open WebSocket Connection
      ws.current = new WebSocket("ws://localhost:8001/ws"); // Connect to FastAPI WebSocket server

      ws.current.onmessage = (event) => {
        const data = JSON.parse(event.data); // Parse JSON response
        if (data.students) {
          const detectedFaces = data.students.map((student) => {
            const [x, y, w, h] = student.bbox;
            return {
              x,
              y,
              w: w - x, // Convert width from right-left
              h: h - y, // Convert height from bottom-top
              name: `${student.name} ${student.surname}`, // Combine full name
              student_id: student.student_id,
            };
          });
          setFaces(detectedFaces);
        }
      };

      ws.current.onerror = (error) => console.error("WebSocket Error:", error);

      // Send frames periodically (every 100ms)
      const sendFrame = () => {
        if (ws.current.readyState === WebSocket.OPEN && videoRef.current) {
          const canvas = document.createElement("canvas");
          const ctx = canvas.getContext("2d");

          canvas.width = videoRef.current.videoWidth;
          canvas.height = videoRef.current.videoHeight;
          ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);

          canvas.toBlob((blob) => {
            if (blob) {
              ws.current.send(blob);
            }
          }, "image/jpeg");
        }
        // setTimeout(sendFrame, 600);
        requestAnimationFrame(sendFrame);
      };

      sendFrame();
    });

    return () => {
      if (ws.current) ws.current.close();
    };
  }, []);

  // Draw face rectangles on canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    const drawBoxes = () => {
      if (!canvas || !ctx || !videoRef.current) return;

      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.strokeStyle = "red";
      ctx.lineWidth = 2;
      ctx.font = "18px Arial";
      ctx.fillStyle = "red";

      faces.forEach(({ x, y, w, h, name }) => {
        ctx.strokeRect(x, y, w, h);
        ctx.fillText(name, x + 5, y - 5);
      });

      requestAnimationFrame(drawBoxes);
    };

    drawBoxes();
  }, [faces]);

  return (
    <div style={{ position: "relative" }}>
      <video ref={videoRef} autoPlay playsInline style={{ width: "100%" }} />
      <canvas
        ref={canvasRef}
        style={{ position: "absolute", top: 0, left: 0, width: "100%" }}
      />
    </div>
  );
};

export default FaceRecognition;
