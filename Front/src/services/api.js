import axios from "axios";
import Cookies from "js-cookie";

// Create an Axios instance with baseURL
const api = axios.create({
  baseURL: "http://localhost:8000", // Your API base URL
  headers: { "Content-Type": "application/json" },
});

// Function to get a new access token using the refresh token
const refreshToken = async () => {
  const response = await axios.post("/api/refresh-token", {
    refresh_token: Cookies.get("refresh_token"),
  });
  return response.data.access_token;
};

// Axios interceptor to handle expired access token
api.interceptors.response.use(
  (response) => response, // If the response is successful, return it
  async (error) => {
    if (error.response && error.response.status === 401) {
      // If the error is Unauthorized (token expired), try to refresh the token
      try {
        const newAccessToken = await refreshToken();
        // Save the new access token in the cookie
        Cookies.set("access_token", newAccessToken, {
          expires: 1 / 24, // 1 hour expiration time
          secure: true,
          sameSite: "Strict",
        });
        // Retry the original request with the new token
        error.config.headers["Authorization"] = `Bearer ${newAccessToken}`;
        return axios(error.config);
      } catch (refreshError) {
        console.error("Refresh token failed", refreshError);
        // Redirect to login if refresh token fails
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
