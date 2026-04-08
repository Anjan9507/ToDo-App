import "./TaskList.css"

function TaskList({ tasks }) {
	if (!tasks.length) {
		return <p className="empty">No tasks yet.</p>
	}

	return (
		<div className="task-list">

			{tasks.map(task => (
				<div key={task.id} className="task-card">

					<div className="task-header">
						<h4>{task.title}</h4>

						<span className={`status ${task.status}`}>
							{task.status}
						</span>
					</div>

					<p className="task-desc">
						{task.description}
					</p>

					<p className="task-date">
						Due: {new Date(task.due_date).toLocaleDateString()}
					</p>

				</div>
			))}

		</div>
	)
}

export default TaskList