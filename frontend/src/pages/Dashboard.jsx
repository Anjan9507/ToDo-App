import { useEffect, useState } from "react"
import Layout from "../components/Layout"
import AddTask from "../components/AddTask"
import TaskList from "../components/TaskList"
import { getTasks, deleteTask, getPendingTasks, getOverdueTasks, getCompletedTasks, searchTasks } from "../api/tasks"
import "./Dashboard.css"
import EditTaskModal from "../components/EditTaskModal"
import toast from "react-hot-toast"

function Dashboard() {
	const [tasks, setTasks] = useState([])

	const [filter, setFilter] = useState("all")

	const [error, setError] = useState("")

	const [search, setSearch] = useState("")

	const [editingTask, setEditingTask] = useState(null)

	useEffect(() => {
		loadTasks()
	}, [])

	useEffect(() => {
		const delayDebounce = setTimeout(async () => {
			if(search.trim() === "") {
				loadTasks(filter)
				return
			}

			try {
				const data = await searchTasks(search)
				setTasks(data)
			} catch (err) {
				setError("Search Failed")
			}
		}, 400)

		return () => clearTimeout(delayDebounce)
	}, [search, filter])

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

			toast.success("Task Deleted")

		} catch (err) {
			toast.error("Failed to delete task")
		}
	}

	const handleUpdate = (updatedTask) => {
		setTasks(prev => prev.map(task => task.id === updatedTask.id ? updatedTask : task))
	}

	const handleEdit = (task) => {
		setEditingTask(task)
	}

	return (
		<Layout>
			<div className="dashboard-container">

				<div className="card">
					<h1>Dashboard</h1>
					<p>Welcome! You are logged in</p>
				</div>

				{error && <p style={{ color: "#ef4444" }}>{error}</p>}

				<input 
					type="text"
					placeholder="Search tasks..." 
					className="task-search"
					value={search}
					onChange={(e) => setSearch(e.target.value)}
				/>

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

					<TaskList 
						tasks={tasks} 
						onDelete={handleDelete} 
						onUpdate={handleUpdate} 
						onEdit={handleEdit}
					/>
				</div>

				{editingTask && (
					<EditTaskModal 
						task={editingTask}
						onClose={() => setEditingTask(null)}
						onUpdate={handleUpdate}
					/>
				)}
			</div>
		</Layout>

	)
}

export default Dashboard