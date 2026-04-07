import Layout from "../components/Layout"
import "./Dashboard.css"

function Dashboard() {
	return (
		<Layout>
			<div className="dashboard-container">

				<div className="card">
					<h1>Dashboard</h1>
					<p>Welcome! You are logged in</p>
				</div>

				<div className="card">
					<h2>Your Tasks</h2>
					<p>No tasks yet. Start adding tasks</p>
				</div>
			</div>
		</Layout>

	)
}

export default Dashboard