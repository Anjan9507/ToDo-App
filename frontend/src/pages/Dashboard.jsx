import { useNavigate } from "react-router-dom"
import { logoutUser } from "../api/auth"

function Dashboard() {
	const navigate = useNavigate()

	const handleLogout = async () => {
		await logoutUser()

		localStorage.removeItem("access_token")
		
		navigate("/login")
	}

	return (
		<div style={{ color: "white", padding: "20px" }}>
			<h1>Dashboard</h1>

			<p>Welcome! You are logged in</p>

			<button onClick={handleLogout}>
				Logout
			</button>
		</div>
	)
}

export default Dashboard