import axios, { AxiosInstance } from "axios";

// Base API URL from environment or default
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api/v1";

// Create Axios instance with base configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor for adding token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

function isAuthPage() {
  const path = window.location.pathname;
  return path === "/login" || path === "/register";
}

function isAuthApiRequest(config: any) {
  // Prevent redirect for login/register API calls
  return (
    config.url?.includes("/auth/login") ||
    config.url?.includes("/auth/register")
  );
}

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (
      error.response?.status === 401 &&
      !isAuthPage() &&
      !isAuthApiRequest(originalRequest)
    ) {
      localStorage.removeItem("token");
      // In a React SPA, you would use navigate('/login') from a context or event bus
      // Here, fallback to full reload for robustness
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default apiClient;
