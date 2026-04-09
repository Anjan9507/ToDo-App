import { useState } from "react"
import { updateTask } from "../api/tasks"
import toast from "react-hot-toast"
import "./EditTaskModal.css"

function EditTaskModal({ task, onClose, onUpdate }) {
	const [title, setTitle] = useState(task.title)
	const [description, setDescription] = useState(task.description)
	const [dueDate, setDueDate] = useState(task.due_date.split("T")[0])
	const [status, setStatus] = useState(task.status)

	const handleSubmit = async (e) => {
		e.preventDefault()

		try {
			const updatedTask = await updateTask(task.id, {
				title,
				description,
				status,
				due_date: dueDate
			})

			onUpdate(updatedTask)
			toast.success("Task Updated")
			onClose()

		} catch (err) {
			toast.error("Failed to update task")
		}
	}

	return (
		<div className="modal-overlay" onClick={onClose}>

			<div className="modal" onClick={(e) => e.stopPropagation()}>
				<h3>Edit Task</h3>

				<form onSubmit={handleSubmit}>

					<input
						type="text"
						value={title}
						onChange={(e) => setTitle(e.target.value)}
					/>

					<input
						type="text"
						value={description}
						onChange={(e) => setDescription(e.target.value)}
					/>

					<input
						type="date"
						value={dueDate}
						onChange={(e) => setDueDate(e.target.value)}
					/>

					<select
						value={status}
						onChange={(e) => setStatus(e.target.value)}
					>
						<option value="pending">Pending</option>
						<option value="completed">Completed</option>
						<option value="overdue">Overdue</option>
					</select>

					<div className="modal-actions">
						<button type="submit">
							Save
						</button>

						<button
							type="button"
							onClick={onClose}
							className="cancel-btn"
						>
							Cancel
						</button>
					</div>
				</form>
			</div>
		</div>
	)
}

export default EditTaskModal