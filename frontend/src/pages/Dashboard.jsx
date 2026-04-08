import { useEffect, useState } from "react"
import Layout from "../components/Layout"
import AddTask from "../components/AddTask"
import TaskList from "../components/TaskList"
import { getTasks, deleteTask, getPendingTasks, getOverdueTasks, getCompletedTasks } from "../api/tasks"
import "./Dashboard.css"

function Dashboard() {
	const [tasks, setTasks] = useState([])

	const [filter, setFilter] = useState("all")

	const [error, setError] = useState("")

	useEffect(() => {
		loadTasks()
	}, [])

	const loadTasks = async (selectedFilter = "all") => {
		try {
			let data = []

			if (selectedFilter === "pending") {
				data = await getPendingTasks()
			} else if (selectedFilter === "completed") {
				data = await getCompletedTasks()
			} else if (selectedFilter === "overdue") {
				data = await getOverdueTasks()
			} else {
				data = await getTasks()
			}

			setTasks(data)
			setFilter(selectedFilter)

		} catch (err) {
			setError("Failed to load tasks")
		}
	}

	const handleTaskAdded = (task) => {
		setTasks(prev => [task, ...prev])
	}

	const handleDelete = async (id) => {
		try {
			await deleteTask(id)

			setTasks(prev => prev.filter(task => task.id !== id))

		} catch (err) {
			setError("Failed to delete task")
		}
	}

	const handleUpdate = (updatedTask) => {
		setTasks(prev => prev.map(task => task.id === updatedTask.id ? updatedTask : task))
	}

	return (
		<Layout>
			<div className="dashboard-container">

				<div className="card">
					<h1>Dashboard</h1>
					<p>Welcome! You are logged in</p>
				</div>

				{error && <p style={{ color: "#ef4444" }}>{error}</p>}

				<div className="task-filters">

					<button
						className={filter === "all" ? "active" : ""}
						onClick={() => loadTasks("all")}
					>
						All
					</button>

					<button
						className={filter === "pending" ? "active" : ""}
						onClick={() => loadTasks("pending")}
					>
						Pending
					</button>

					<button
						className={filter === "completed" ? "active" : ""}
						onClick={() => loadTasks("completed")}
					>
						Completed
					</button>

					<button
						className={filter === "overdue" ? "active" : ""}
						onClick={() => loadTasks("overdue")}
					>
						Overdue
					</button>

				</div>

				<div className="card">
					<h2>Your Tasks</h2>

					<AddTask onTaskAdded={handleTaskAdded} />

					<TaskList tasks={tasks} onDelete={handleDelete} onUpdate={handleUpdate} />
				</div>
			</div>
		</Layout>

	)
}

export default Dashboard