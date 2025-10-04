import axios from "axios";

const API_BASE = ""|| "http://127.0.0.1:8000/";
const axiosInstance = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

// attach access token
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// response interceptor: refresh logic
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (!originalRequest) return Promise.reject(error);

    // avoid infinite loop
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem("refresh");
        if (!refreshToken) {
          // no refresh token -> logout
          localStorage.removeItem("access");
          localStorage.removeItem("refresh");
          return Promise.reject(error);
        }

        const resp = await axios.post(`${API_BASE}/api/token/refresh/`, {
          refresh: refreshToken,
        });

        if (resp.status === 200) {
          localStorage.setItem("access", resp.data.access);
          // update header and retry
          originalRequest.headers.Authorization = `Bearer ${resp.data.access}`;
          return axiosInstance(originalRequest);
        }
      } catch (refreshErr) {
        // refresh failed: clear storage and redirect to login (or let caller handle)
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        window.location.href = "/login";
        return Promise.reject(refreshErr);
      }
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;
