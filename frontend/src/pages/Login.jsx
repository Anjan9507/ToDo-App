import { useState } from "react"
import { useNavigate, Navigate, Link } from "react-router-dom"
import { loginUser } from "../api/auth"
import toast from "react-hot-toast"
import "./Login.css"

function Login() {
	const navigate = useNavigate()

	const [email, setEmail] = useState("")
	const [password, setPassword] = useState("")

	const [loading, setLoading] = useState(false)

	const token = localStorage.getItem("access_token")
	if (token) {
		return <Navigate to="/dashboard" />
	}

	const handleSubmit = async (e) => {
		e.preventDefault()

		setLoading(true)

		try {
			const data = await loginUser(email, password)

			localStorage.setItem("access_token", data.access_token)

			toast.success("Logged in Successfully")

			navigate("/dashboard")
		} catch (err) {
			toast.error("Invalid Credentials")
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

				<button type="submit" disabled={loading}>
					{loading ? "Logging in..." : "Login"}
				</button>

				<p className="auth-link">
					Don't have an account? <Link to="/register">Register</Link>
				</p>
			</form>
		</div>
	)
}

export default Login
