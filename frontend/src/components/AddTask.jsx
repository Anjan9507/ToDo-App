import { useState } from "react"
import { createTask } from "../api/tasks"
import "./AddTask.css"

function AddTask({ onTaskAdded }) {
	const [title, setTitle] = useState("")
	const [description, setDescription] = useState("")
	const [dueDate, setDueDate] = useState("")

	const [error, setError] = useState("")

	const handleSubmit = async (e) => {
		e.preventDefault()

		try {
			const newTask = await createTask({
				title,
				description,
				due_date: dueDate
			})

			onTaskAdded(newTask)

			setTitle("")
			setDescription("")
			setDueDate("")

		} catch (err) {
				setError("Failed to add task")
				setTimeout(() => {
					setError("")
				}, 3000)
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
				onChange={(e) => {setDueDate(e.target.value)}}
			/>

			<button type="submit">
				Add Task
			</button>

			{error && <p style={{ color: "#ef4444" }}>{error}</p>}
		</form>
	)
}

export default AddTask