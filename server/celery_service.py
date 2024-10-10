import time
from celery import shared_task

from app.worker import celery_init_app
from server import app

celery_app = celery_init_app(app)

# Tasks
from app.tasks import add_together, send_daily_reminder

# Scheduled Tasks (Celery Beat)
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, send_daily_reminder.s(), name='Daily influencer reminder.')
