from fastapi import APIRouter, Depends, status
from app.services import task_service
from app.schemas.task_schema import TaskCreate, TaskCreateResponse, TaskUpdate, TaskUpdateResponse
from app.database.db import get_db
from app.services.security_service import get_current_user

router = APIRouter()

@router.get("/tasks", status_code=status.HTTP_200_OK)
def get_all_tasks(db=Depends(get_db), current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]
    return task_service.get_tasks(db, user_id)


@router.get("/tasks/pending", status_code=status.HTTP_200_OK)
def get_only_pending_tasks(db=Depends(get_db), current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]
    return task_service.get_pending_tasks(db, user_id)


@router.get("/tasks/completed", status_code=status.HTTP_200_OK)
def get_only_completed_tasks(db=Depends(get_db), current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]
    return task_service.get_completed_tasks(db, user_id)


@router.get("/tasks/overdue", status_code=status.HTTP_200_OK)
def get_only_overdue_tasks(db=Depends(get_db), current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]
    return task_service.get_overdue_tasks(db, user_id)


@router.get("/tasks/search", status_code=status.HTTP_200_OK)
def get_searched_tasks(task_title: str, db=Depends(get_db), current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]
    return task_service.search_tasks(db, user_id, task_title)


@router.post("/tasks/add", response_model=TaskCreateResponse, status_code=status.HTTP_201_CREATED)
def add_tasks(data: TaskCreate, db=Depends(get_db), current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]
    return task_service.insert_tasks(db, user_id, data)


@router.put("/tasks/update/{id}", response_model=TaskUpdateResponse, status_code=status.HTTP_200_OK)
def update_task_details(id: int, data: TaskUpdate, db=Depends(get_db), current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]
    return task_service.update_tasks(db, id, user_id, data)


@router.delete("/tasks/delete/{id}", status_code=status.HTTP_200_OK)
def delete_task(id: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]
    return task_service.remove_task(db, id, user_id)

