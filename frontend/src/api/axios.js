import axios from "axios"
import toast from "react-hot-toast"

const api = axios.create({
	baseURL: "https://todo-backend-6b91.onrender.com",
	withCredentials: true
})


api.interceptors.request.use(
	(config) => {
		const token = localStorage.getItem("access_token")

		if (token) {
			config.headers.Authorization = `Bearer ${token}`
		}

		return config
	},
	(error) => Promise.reject(error)
)


api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config || {}

    if(error.response?.status === 429) {
      toast.error("Too many attempts. Try again later.")
    } 

    if (
			error.response?.status === 401 && 
			!originalRequest._retry &&
			!originalRequest.url.includes("/login") &&
			!originalRequest.url.includes("/refresh")
		) {
      originalRequest._retry = true

      try {
        const res = await api.post("/refresh")

        const newToken = res.data.access_token

        localStorage.setItem("access_token", newToken)

        originalRequest.headers.Authorization = `Bearer ${newToken}`

        return api(originalRequest)

      } catch (err) {
        localStorage.removeItem("access_token")
        window.location.href = "/login"
      }
    }

    return Promise.reject(error)
  }
)

export default api