from flask_mail import Mail, Message

mail = Mail()

def send_email_reminder(influencer):
    sponsors = '\n'.join(f'{idx + 1}. ' + sponsor_name for (idx, sponsor_name) in enumerate(influencer['pending_ads_sponsor_names']))
    msg = Message(
        subject="Reminder: Pending Ad Requests",
        recipients=[influencer['email']],
        body=f"Hi {influencer['name']},\n\nYou have pending ad requests from:\n{sponsors}\n\nPlease visit our website to take action.\nAlso don't forget to check out the Public Campaigns listed on our website.\n\nThanks,\nTeam SponsorConnect"
    )
    mail.send(msg)
