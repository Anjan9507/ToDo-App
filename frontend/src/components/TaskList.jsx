import "./TaskList.css"
import { updateTask } from "../api/tasks"
import toast from "react-hot-toast"

function TaskList({ tasks, onDelete, onUpdate, onEdit }) {
	if (!tasks.length) {
		return <p className="empty">No tasks found.</p>
	}

	const toggleStatus = async (task) => {
		try {
			const newStatus = task.status === "completed" ? "pending" : "completed"

			const updatedTask = await updateTask(task.id, {
				...task,
				status: newStatus
			})
			onUpdate(updatedTask)
			toast.success("Task status updated")

		} catch (err) {
			toast.error("Status update failed")
		}
	}

	return (
		<div className="task-list">

			{tasks.map(task => (
				<div key={task.id} className="task-card">

					<div className="task-header">
						<h4>{task.title}</h4>

						<div className="task-actions">

							<span
								className={`status ${task.status}`}
								onClick={() => toggleStatus(task)}
							>
								{task.status}
							</span>

							<button className="edit-btn" onClick={() => onEdit(task)}>
								Edit
							</button>

							<button
								className="delete-btn"
								onClick={() => onDelete(task.id)}
							>
								Delete
							</button>

						</div>

					</div>

					<p className="task-desc">{task.description}</p>

					<p className="task-date">
						Due: {new Date(task.due_date).toLocaleDateString()}
					</p>

				</div>
			))}

		</div>
	)
}

export default TaskList
