import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { resetPassword } from "../api/auth"
import toast from "react-hot-toast"
import "./ResetPassword.css"

function ResetPassword() {
	const navigate = useNavigate()

	const [token, setToken] = useState("")
	const [password, setPassword] = useState("")
	const [loading, setLoading] = useState(false)

	const handleSubmit = async (e) => {
		e.preventDefault()

		setLoading(true)

		try {
			await resetPassword(token, password)

			toast.success("Password reset successfull")

			navigate("/login")

		} catch (err) {
			toast.error(err.message)

		} finally {
			setLoading(false)
		}
	}

	return (
		<div className="container">

			<form className="login-card" onSubmit={handleSubmit}>

				<h2 className="title">Reset Password</h2>

				<input
					type="text"
					placeholder="Reset Token"
					value={token}
					onChange={(e) => setToken(e.target.value)}
					required
				/>

				<input
					type="password"
					placeholder="New Password"
					value={password}
					onChange={(e) => setPassword(e.target.value)}
					required
				/>

				<button type="submit" disabled={loading}>
					{loading ? "Resetting..." : "Reset Password"}
				</button>
			</form>
		</div>
	)
}

export default ResetPassword