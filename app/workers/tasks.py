from app.core.celery_app import celery_app
from app.database.db import get_db
from app.services.whatsapp_service import send_whatsapp_message
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
                    users.phone AS phone
                FROM tasks
                JOIN users
                    ON tasks.user_id = users.id
                WHERE tasks.due_date = %s
                AND tasks.status != 'completed'
                AND tasks.reminder_sent = FALSE
            """, (today,))
        
        tasks = cursor.fetchall()

        for task_id, task_title, due_date, phone in tasks:
            message = f"""
Reminder 🚨

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
