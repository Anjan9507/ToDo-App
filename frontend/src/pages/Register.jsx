import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import { registerUser } from "../api/auth"
import toast from "react-hot-toast"
import "./Register.css"

function Register() {
	const navigate = useNavigate()

	const [name, setName] = useState("")
	const [email, setEmail] = useState("")
	const [phone, setPhone] = useState("")
	const [password, setPassword] = useState("")

	const [loading, setLoading] = useState(false)

	const handleSubmit = async (e) => {
		e.preventDefault()

		setLoading(true)

		try {
			await registerUser({
				name,
				email,
				phone,
				password
			})

			toast.success("Account created successfully")

			navigate("/login")

		} catch (err) {
			toast.error("Register Failed")

		} finally {
			setLoading(false)
		}
	}

	return (
		<div className="container">

			<form onSubmit={handleSubmit} className="login-card">

				<h2 className="title">Create Account</h2>

				<input
					type="text"
					placeholder="Full Name"
					value={name}
					onChange={(e) => setName(e.target.value)}
					required
				/>

				<input
					type="email"
					placeholder="Email"
					value={email}
					onChange={(e) => setEmail(e.target.value)}
					required
				/>

				<input
					type="text"
					placeholder="Phone"
					value={phone}
					onChange={(e) => setPhone(e.target.value)}
				/>

				<input
					type="password"
					placeholder="Password"
					value={password}
					onChange={(e) => setPassword(e.target.value)}
					required
				/>

				<button type="submit" disabled={loading}>
					{loading ? "Creating Account..." : "Register"}
				</button>

				<p className="auth-link">
					Already have an account? <Link to="/login">Login</Link>
				</p>
			</form>
		</div>
	)
}

export default Register