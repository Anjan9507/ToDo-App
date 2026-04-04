from fastapi import HTTPException

def update_overdue_tasks(db, user_id: int):
    with db.cursor() as cursor:
        cursor.execute("UPDATE tasks SET status = 'overdue' WHERE user_id = %s AND due_date < NOW() AND status = 'pending'",
                       (user_id,))


def get_tasks(db, user_id: int):
    cursor = db.cursor()
    try:
        update_overdue_tasks(db, user_id)
        cursor.execute(
             """SELECT 
                    id, title, description, status, due_date 
                FROM tasks 
                WHERE user_id = %s
            """, (user_id,))
        
        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(
                status_code=404,
                detail="Tasks not found"
            )
        
        tasks = []

        for id, title, description, status, due_date in rows:
            tasks.append({
                "id": id,
                "title": title,
                "description": description,
                "status": status,
                "due_date": due_date
            })

        return tasks
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def get_pending_tasks(db, user_id: int):
    cursor = db.cursor()
    try:
        update_overdue_tasks(db, user_id)
        cursor.execute(
             """SELECT
                    id, title, description, status, due_date
                FROM tasks
                WHERE user_id = %s
                AND status = 'pending'
            """, (user_id,))
        
        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(
                status_code=404,
                detail="No pending tasks found"
            )
        
        tasks = []

        for id, title, description, status, due_date in rows:
            tasks.append({
                "id": id,
                "title": title,
                "description": description,
                "status": status,
                "due_date": due_date
            })

        return tasks
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def get_completed_tasks(db, user_id: int):
    cursor = db.cursor()
    try:
        update_overdue_tasks(db, user_id)
        cursor.execute(
             """SELECT
                    id, title, description, status, due_date
                FROM tasks
                WHERE user_id = %s
                AND status = 'completed'
            """, (user_id,))
        
        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(
                status_code=404,
                detail="No completed tasks found"
            )
        
        tasks = []

        for id, title, description, status, due_date in rows:
            tasks.append({
                "id": id,
                "title": title,
                "description": description,
                "status": status,
                "due_date": due_date
            })

        return tasks
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def get_overdue_tasks(db, user_id: int):
    cursor = db.cursor()
    try:
        update_overdue_tasks(db, user_id)
        cursor.execute(
             """SELECT
                    id, title, description, status, due_date
                FROM tasks
                WHERE user_id = %s
                AND status = 'overdue'
            """, (user_id,))
        
        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(
                status_code=404,
                detail="No overdue tasks found"
            )
        
        tasks = []

        for id, title, description, status, due_date in rows:
            tasks.append({
                "id": id,
                "title": title,
                "description": description,
                "status": status,
                "due_date": due_date
            })

        return tasks
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def search_tasks(db, user_id: int, task_title: str):
    cursor = db.cursor()
    try:
        update_overdue_tasks(db, user_id)
        cursor.execute(
             """SELECT
                    id, title, description, status, due_date
                FROM tasks
                WHERE user_id = %s
                AND (title ILIKE %s OR description ILIKE %s)
                ORDER BY id
            """, (user_id, f"%{task_title}%", f"%{task_title}%"))
        
        rows = cursor.fetchall()
        
        tasks = []

        for id, title, description, status, due_date in rows:
            tasks.append({
                "id": id,
                "title": title,
                "description": description,
                "status": status,
                "due_date": due_date
            })

        return tasks
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()



def insert_tasks(db, user_id: int, data):
    cursor = db.cursor()
    try:
        cursor.execute("""INSERT INTO tasks (user_id, title, description, due_date) VALUES (%s, %s, %s, %s) 
                       RETURNING id, title, description, due_date
                       """, (user_id, data.title, data.description, data.due_date))
        
        row = cursor.fetchone()

        if not row:
            raise HTTPException(
                status_code=400,
                detail="Invalid Request"
            )

        db.commit()

        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "due_date": row[3]
        }
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def update_tasks(db, id: int, user_id: int, data):
    cursor = db.cursor()
    try:
        cursor.execute(
             """UPDATE tasks 
                SET title = %s, description = %s, status = %s, due_date = %s
                WHERE id = %s
                AND user_id = %s
                RETURNING id, title, description, status, due_date
            """, (data.title, data.description, data.status, data.due_date, id, user_id))
        
        row = cursor.fetchone()

        if not row:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )
        
        db.commit()

        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "due_date": row[4]
        }
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def remove_task(db, id: int, user_id: int):
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s RETURNING id, title", (id, user_id))

        row = cursor.fetchone()

        if not row:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )
        
        db.commit()

        return {
            "id": row[0],
            "title": row[1],
            "message": "Task removed successfully"
        }
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


