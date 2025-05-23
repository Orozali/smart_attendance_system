import { useEffect, useState } from "react";
import api from "../../services/api";
import Cookies from "js-cookie";

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const accessToken = Cookies.get("access_token");
      if (!accessToken) {
        setError("Access token is missing");
        setLoading(false);
        return;
      }
      try {
        const response = await api.get(
          "https://40c8-178-217-174-2.ngrok-free.app/teacher/main-info",
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              "Content-Type": "application/json",
            },
          }
        );
        setData(response.data);
      } catch (err) {
        setError("Failed to fetch data!");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading)
    return <div className="text-center mt-10 text-lg">Loading...</div>;
  if (error)
    return <div className="text-center mt-10 text-red-500">{error}</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold text-center text-green-700">
        Студенттер менен иштөө маалымат системасына кош келиңиздер!
      </h1>

      <h2 className="mt-4 text-lg font-bold text-green-800">
        Др. {data.teacher_name}
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-6">
        {/* Students Count */}
        <div className="bg-blue-600 text-white p-6 rounded-lg shadow-md text-center">
          <h3 className="text-3xl font-bold">{data.studentCount}</h3>
          <p>Учурдагы семестрдa Сиз сабак берген студенттердин саны</p>
          <a href="#" className="text-white underline">
            Сабактардын тизмеси 📎
          </a>
        </div>

        {/* Lessons Count */}
        <div className="bg-green-600 text-white p-6 rounded-lg shadow-md text-center">
          <h3 className="text-3xl font-bold">{data.lessonCount}</h3>
          <p>Учурдагы семестрдa Сиз берген сабактардын саны</p>
          <a href="#" className="text-white underline">
            Сабактардын тизмеси 📎
          </a>
        </div>

        {/* Departments Count */}
        <div className="bg-yellow-500 text-white p-6 rounded-lg shadow-md text-center">
          <h3 className="text-3xl font-bold">{data.departmentCount}</h3>
          <p>Учурдагы семестрдa Сиз сабак берген бөлүм саны</p>
          <a href="#" className="text-white underline">
            Сабактардын тизмеси 📎
          </a>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
