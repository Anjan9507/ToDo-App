from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv
import ssl

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.autodiscover_tasks(["app.workers"])

celery_app.conf.update(
    broker_use_ssl={
        "ssl_cert_reqs": ssl.CERT_NONE
    },
    redis_backend_use_ssl={
        "ssl_cert_reqs": ssl.CERT_NONE
    },
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,

    beat_schedule={
        "check_due_tasks": {
            "task": "app.workers.tasks.check_due_tasks",
            "schedule": 60.0,
        },
        "update-overdue-tasks": {
            "task": "app.workers.tasks.update_overdue_tasks",
            "schedule": crontab(hour=0, minute=0),
        }
    }
)
