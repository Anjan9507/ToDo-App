import { useState } from "react"
import { forgotPassword } from "../api/auth"
import { useNavigate } from "react-router-dom"
import toast from "react-hot-toast"
import { Link } from "react-router-dom"
import "./ForgotPassword.css"

function ForgotPassword() {
	const navigate = useNavigate()

	const [email, setEmail] = useState("")

	const [loading, setLoading] = useState(false)

	const handleSubmit = async (e) => {
		e.preventDefault()

		setLoading(true)

		try {
			const data = await forgotPassword(email)

			toast.success("Reset token generated")

			navigate("/reset-password")

			console.log("RESET TOKEN: ", data.reset_token)

		} catch (err) {
			toast.error(err.message)

		} finally {
			setLoading(false)
		}
	}

	return (
		<div className="container">

			<form onSubmit={handleSubmit} className="login-card">

				<h2 className="title">Forgot Password</h2>

				<input 
					type="email" 
					placeholder="Enter your email"
					value={email}
					onChange={(e) => setEmail(e.target.value)}
					required
				/>

				<button type="submit" disabled={loading}>
					{loading ? "Sending..." : "Send Reset Link"}
				</button>

				<p className="auth-link">
					<Link to="/login">Back to Login</Link>
				</p>
			</form>
		</div>
	)
}

export default ForgotPassword