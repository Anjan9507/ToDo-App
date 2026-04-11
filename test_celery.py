from app.services.tasks import test_task

result = test_task.delay()

print("Task sent: ", result.id)