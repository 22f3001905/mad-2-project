import time
from celery import shared_task

from app.mail import send_email_reminder, send_email_report
from app.utils import get_influencers_with_pending_requests, get_sponsors

@shared_task(ignore_result=False)
def add_together(x, y):
    print("Celery Function Triggered: add_together")
    time.sleep(5)  # Mimic a long running task.
    return x + y

@shared_task(ignore_result=True)
def send_daily_reminder():
    try:
        print("Celery Function Triggered: send_daily_reminder")
        influencers = get_influencers_with_pending_requests()

        for influencer in influencers:
            print('Sending a mail to:', influencer['name'])
            send_email_reminder(influencer)
        
    except Exception as e:
        print('Error in send_daily_reminder:', e)

@shared_task(ignore_result=True)
def send_monthly_sponsor_report():
    try:
        print('Celery Funcion Triggered: send_monthly_sponsor_report')
        sponsors = get_sponsors()

        for sponsor in sponsors:
            print('Sending report to:', sponsor['name'])
            send_email_report(sponsor)

    except Exception as e:
        print('Error in send_monthly_sponsor_report:', e)

@shared_task(ignore_result=False)
def export_campaigns_data(campaigns):
    print("Celery Function Triggered: export_campaigns_data")
    
    print(campaigns)
    time.sleep(30)

    return { 'message': '.csv file is ready.', 'file_link': 'some_linke!!!!!!!!!!!' }
