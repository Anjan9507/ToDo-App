from backend.core.celery_app import celery_app
from backend.database.db import get_db
from backend.services.whatsapp_service import send_whatsapp_message
from datetime import date

@celery_app.task
def check_due_tasks():
    db=next(get_db())
    cursor = db.cursor()

    try:
        today = date.today()

        cursor.execute(
             """SELECT
                    tasks.id AS task_id,
                    tasks.title AS task_title,
                    tasks.due_date AS due_date,
                    users.name AS name,
                    users.phone AS phone
                FROM tasks
                JOIN users
                    ON tasks.user_id = users.id
                WHERE tasks.due_date = %s
                AND tasks.status != 'completed'
                AND tasks.reminder_sent = FALSE
            """, (today,))
        
        tasks = cursor.fetchall()

        for task_id, task_title, due_date, name, phone in tasks:
            message = f"""
Reminder 🚨
Hi {name}

Task: {task_title}
Due today: {due_date.strftime("%B %d, %Y")}

Don't forget to complete it!
"""
            send_whatsapp_message(phone, message)

            cursor.execute("UPDATE tasks SET reminder_sent = TRUE WHERE id = %s", (task_id,))
        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


@celery_app.task
def update_overdue_tasks():
    db=next(get_db())
    cursor = db.cursor()

    try:
        today = date.today()

        cursor.execute("UPDATE tasks SET status = 'overdue' WHERE due_date < %s AND status = 'pending'", (today,))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()