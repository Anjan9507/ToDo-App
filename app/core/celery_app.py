from celery import Celery
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

celery_app.autodiscover_tasks(["app.services"])

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
        "run-test-task-every-10-seconds": {
            "task": "app.services.tasks.test_task",
            "schedule": 10.0,
        },
    }
)
