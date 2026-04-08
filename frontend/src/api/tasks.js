import api from "./axios"

export const getTasks = async () => {
    const response = await api.get("/tasks")
    return response.data
}

export const createTask = async (task) => {
    const response = await api.post("/tasks/add", task)
    return response.data
}
