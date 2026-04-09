import { useState } from "react"
import { createTask } from "../api/tasks"
import toast from "react-hot-toast"
import "./AddTask.css"

function AddTask({ onTaskAdded }) {
	const [title, setTitle] = useState("")
	const [description, setDescription] = useState("")
	const [dueDate, setDueDate] = useState("")

	const handleSubmit = async (e) => {
		e.preventDefault()

		try {
			const newTask = await createTask({
				title,
				description,
				due_date: dueDate
			})

			onTaskAdded(newTask)

			toast.success("Task Created")

			setTitle("")
			setDescription("")
			setDueDate("")

		} catch (err) {
			toast.error("Failed to add task")
		}
	}

	return (
		<form onSubmit={handleSubmit} className="add-task-form">

			<input
				type="text"
				placeholder="Task Title"
				value={title}
				onChange={(e) => setTitle(e.target.value)}
				required
			/>

			<input
				type="text"
				placeholder="Description"
				value={description}
				onChange={(e) => setDescription(e.target.value)}
			/>

			<input
				type="date"
				value={dueDate}
				onChange={(e) => { setDueDate(e.target.value) }}
			/>

			<button type="submit">
				Add Task
			</button>

		</form>
	)
}

export default AddTask