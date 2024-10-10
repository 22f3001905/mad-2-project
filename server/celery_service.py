import time
from celery import shared_task

from app.worker import celery_init_app
from server import app

celery_app = celery_init_app(app)

# Tasks
from app.tasks import add_together

# Scheduled Tasks (Celery Beat)
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls add_together(5, 10) every 10 seconds.
    sender.add_periodic_task(10.0, add_together.s(5, 10), name='Add every 10s.')
