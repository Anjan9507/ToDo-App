import api from "./axios"

export const loginUser = async (email, password) => {
	try {
		const response = await api.post("/login", {
			email,
			password
		})

		return response.data
	} catch (err) {
		throw new Error(
			err.response?.data?.detail || "Login Failed"
		)
	}
}

export const registerUser = async (userData) => {
	try {
		const response = await api.post("/register", userData)
		return response.data

	} catch (err) {
		throw new Error(
			err.response?.data?.detail || "Registration failed"
		)
	}
}

export const logoutUser = async () => {
	try {
		await api.post("/logout")
	} catch (err) {
		console.error("Logout failed")
	}
}

export const forgotPassword = async (email) => {
	try {
		const response = await api.post("/forgot-password", { email })
		return response.data
	} catch (err) {
		throw new Error(
			err.response?.data?.detail || "Request failed"
		)
	}
}


export const resetPassword = async (token, newPassword) => {
	try {
		const response = await api.post("/reset-password", {
			token,
			new_password: newPassword
		})
		return response.data
	} catch (err) {
		throw new Error(
			err.response?.data?.detail || "Reset failed"
		)
	}
}



