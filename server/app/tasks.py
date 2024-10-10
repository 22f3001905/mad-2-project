import time
from celery import shared_task

@shared_task(ignore_result=False)
def add_together(x, y):
    print("Celery Function Triggered.")
    time.sleep(5)  # Mimic a long running task.
    return x + y
