import time
from celery import shared_task
from celery.schedules import crontab

from app.worker import celery_init_app
from server import app

celery_app = celery_init_app(app)

# Tasks
from app.tasks import send_daily_reminder, send_monthly_sponsor_report

# Scheduled Tasks (Celery Beat)
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        # 15.0,  # Test
        crontab(hour=17, minute=0),  # 17:00 everyday.
        send_daily_reminder.s(), 
        name='Daily Influencer Reminder'
    )
    sender.add_periodic_task(
        # 30.0,  # Test
        crontab(minute=0, hour=8, day_of_month=1),  # 08:00 on first day of every month.
        send_monthly_sponsor_report.s(),
        name='Montly Sponsor Report'
    )
