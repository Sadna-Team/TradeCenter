import axios from 'axios';

// Create an instance of axios
let apiUrl;

if (typeof window !== 'undefined') {
  apiUrl = process.env.NEXT_PUBLIC_API_URL || `http://${window.location.hostname}:5000`;
} else {
  apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
}

const api = axios.create({
  baseURL: apiUrl,
});

// Add a request interceptor
api.interceptors.request.use(
  function (config) {
    // Do something before request is sent
    const token = sessionStorage.getItem('token'); // Example of getting a token from localStorage
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  function (error) {
    // Do something with request error
    return Promise.reject(error);
  }
);

// Add a response interceptor
api.interceptors.response.use(
  function (response) {
    // Any status code that lie within the range of 2xx cause this function to trigger
    // Do something with response data
    return response;
  },
  function (error) {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    // Do something with response error
    if (error.response.status === 401) {
      // Handle unauthorized access, for example, by redirecting to the login page
    }
    return Promise.reject(error);
  }
);

export default api;
