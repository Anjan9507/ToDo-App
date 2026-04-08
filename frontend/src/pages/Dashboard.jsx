import { useEffect, useState } from "react"
import Layout from "../components/Layout"
import AddTask from "../components/AddTask"
import TaskList from "../components/TaskList"
import { getTasks } from "../api/tasks"
import "./Dashboard.css"

function Dashboard() {
	const [tasks, setTasks] = useState([])

	const [error, setError] = useState("")
	
	useEffect(() => {
		loadTasks()
	}, [])

	const loadTasks = async () => {
		try {
			const data = await getTasks()
			setTasks(data)
		} catch(err) {
			setError("Failed to load tasks")
		}
	}

	const handleTaskAdded = (task) => {
		setTasks(prev => [task, ...prev])
	}

	return (
		<Layout>
			<div className="dashboard-container">

				<div className="card">
					<h1>Dashboard</h1>
					<p>Welcome! You are logged in</p>
				</div>

				{error && <p style={{color: "#ef4444"}}>{error}</p>}

				<div className="card">
					<h2>Your Tasks</h2>

					<AddTask  onTaskAdded={handleTaskAdded} />

					<TaskList tasks={tasks} />
				</div>
			</div>
		</Layout>

	)
}

export default Dashboard