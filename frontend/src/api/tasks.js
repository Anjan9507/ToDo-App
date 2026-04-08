import api from "./axios"

export const getTasks = async () => {
    const response = await api.get("/tasks")
    return response.data
}

export const getPendingTasks = async () => {
  const response = await api.get("/tasks/pending")
  return response.data
}

export const getCompletedTasks = async () => {
  const response = await api.get("/tasks/completed")
  return response.data
}

export const getOverdueTasks = async () => {
  const response = await api.get("/tasks/overdue")
  return response.data
}

export const createTask = async (task) => {
    const response = await api.post("/tasks/add", task)
    return response.data
}

export const deleteTask = async (id) => {
    const response = await api.delete(`/tasks/delete/${id}`)
    return response.data
}

export const updateTask = async (id, taskData) => {
    const response = await api.put(`/tasks/update/${id}`, taskData)
    return response.data
}

export const searchTasks = async (query) => {
    const response = await api.get(`/tasks/search?task_title=${query}`)
    return response.data
}