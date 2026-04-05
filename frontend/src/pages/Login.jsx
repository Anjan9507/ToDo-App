import { useState } from "react"
import { useNavigate, Navigate } from "react-router-dom"
import { loginUser } from "../api/auth"
import "./Login.css"

function Login() {
	const navigate = useNavigate()

	const [email, setEmail] = useState("")
	const [password, setPassword] = useState("")

	const [error, setError] = useState("")
	const [loading, setLoading] = useState(false)

	const token = localStorage.getItem("access_token")
	if (token) {
		return <Navigate to="/dashboard" />
	}

	const handleSubmit = async (e) => {
		e.preventDefault()

		setError("")
		setLoading(true)

		try {
			const data = await loginUser(email, password)

			localStorage.setItem("access_token", data.access_token)

			navigate("/dashboard")
		} catch (err) {
			setError(err.message)
		} finally {
			setLoading(false)
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

				{error && <p className="error">{error}</p>}

				<button type="submit" disabled={loading}>
					{loading ? "Logging in..." : "Login"}
				</button>
			</form>
		</div>
	)
}

export default Login
