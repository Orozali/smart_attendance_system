import axios from "axios";
import Cookies from "js-cookie";
import { BASE_URL } from "../config";

const api = axios.create({
  // baseURL: "http://localhost:8000", // Your API base URL
  baseURL: BASE_URL,     
  headers: { "Content-Type": "application/json", "ngrok-skip-browser-warning": "69420" },
});

const refreshToken = async () => {
  const response = await axios.post(
    `${BASE_URL}/auth/refresh-token`,
    {
      refresh_token: Cookies.get("refresh_token"),
    }
  );
  return response.data.access_token;
};

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    console.log("error:", error);
    if (error.response && error.response.status === 401) {
      try {
        const newAccessToken = await refreshToken();
        Cookies.set("access_token", newAccessToken, {
          expires: 1 / 24,
          secure: true,
          sameSite: "Strict",
        });
        error.config.headers["Authorization"] = `Bearer ${newAccessToken}`;
        return axios(error.config);
      } catch (refreshError) {
        console.error("Refresh token failed", refreshError);
        // Redirect to  if refresh token fails
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
