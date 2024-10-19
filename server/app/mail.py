from flask_mail import Mail, Message
from flask import render_template

mail = Mail()

def send_email_reminder(influencer):
    sponsors = '\n'.join(f'{idx + 1}. ' + sponsor_name for (idx, sponsor_name) in enumerate(influencer['pending_ads_sponsor_names']))
    
    msg = Message(
        subject="Reminder: Pending Ad Requests",
        recipients=[influencer['email']],
        body=f"Hi {influencer['name']},\n\nYou have pending ad requests from:\n{sponsors}\n\nPlease visit our website to take action.\nAlso don't forget to check out the Public Campaigns listed on our website.\n\nThanks,\nTeam SponsorConnect"
    )

    mail.send(msg)

# The activity report can consist of campaign details, how many advertisements done, growth in sales of products due to campaigns, budget used/remaining etc.

def send_email_report(sponsor):
    import os
    # print(os.getcwd())
    # print(os.path.abspath('templates/report.html'))

    msg = Message(
        subject='Monthly Activity Report - SponsorConnect',
        recipients=[sponsor['email']],
        html=render_template('report.html', sponsor=sponsor)
    )

    mail.send(msg)
