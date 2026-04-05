import { useState } from "react"
import { useNavigate, Navigate } from "react-router-dom"
import { loginUser } from "../api/auth"
import "./Login.css"

function Login() {
	const navigate = useNavigate()

	const [email, setEmail] = useState("")
	const [password, setPassword] = useState("")

	const token = localStorage.getItem("access_token")
	if (token) {
		return <Navigate to="/dashboard" />
	}

	const handleSubmit = async (e) => {
		e.preventDefault()

		try {
			const data = await loginUser(email, password)

			localStorage.setItem("access_token", data.access_token)

			console.log("Login Sucess")

			navigate("/dashboard")
		} catch (err) {
			console.error(err.message)
		}
	}

	return (
		<div className="container">
			<form onSubmit={handleSubmit} className="login-card">
				<h2 className="title">Login</h2>

				<input
					type="email"
					placeholder="Enter Email"
					value={email}
					onChange={(e) => setEmail(e.target.value)}
					required
				/>

				<input
					type="password"
					placeholder="Enter Password"
					value={password}
					onChange={(e) => setPassword(e.target.value)}
					required
				/>

				<button type="submit">
					Login
				</button>
			</form>
		</div>
	)
}

export default Login
