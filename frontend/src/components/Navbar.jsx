import { useNavigate } from "react-router-dom"
import { logoutUser } from "../api/auth"
import "./Navbar.css"

function Navbar() {
	const navigate = useNavigate()

	const handleLogout = async () => {
		await logoutUser()
		localStorage.removeItem("access_token")
		navigate("/login")
	}

	return (
		<div className="navbar">
			<h2 className="navbar-title">ToDo App</h2>

			<button onClick={handleLogout} className="logout-btn">
				Logout
			</button>
		</div>
	)
}

export default Navbar