from flask import current_app as app
from flask_security import hash_password

from app.models import db, Influencer, AdRequest

def create_user(email, password, roles: list):
    user_exists = app.security.datastore.find_user(email=email)
    if not user_exists:
        hashed_password = hash_password(password)
        app.security.datastore.create_user(email=email, password=hashed_password, roles=roles)
        return app.security.datastore.find_user(email=email)
    
    return None

def form_hard_coded():
    industry_names = ['Fashion/Apparel', 'Food & Beverage', 'Beauty/Cosmetics', 'Travel', 'Health/Fitness', 'Technology', 'Entertainment', 'Automotive', 'Education', 'Other']
    influencer_category_names = ['Fashion', 'Fitness', 'Travel', 'Food', 'Tech', 'Lifestyle', 'Education', 'Gaming', 'Finance', 'Other']
    campaign_niche_names = ['Social Media Advertising', 'Video Advertising', 'Sponsored Content', 'Affiliate Marketing', 'Sponsored Posts', 'Other']

    return {
        "industry_names": industry_names, 
        "influencer_category_names": influencer_category_names, 
        "campaign_niche_names": campaign_niche_names,
    }

def get_influencers_with_pending_requests():
    ad_requests = db.session.query(AdRequest).all()
    influencers = []

    for ad in ad_requests:
        if ad.status.name != 'Pending' or ad.influencer == None:
            continue

        influ = {
            'id': ad.influencer.id,
            'name': ad.influencer.name,
            'email': ad.influencer.user.email,
        }

        influencer_emails = [influ['email'] for influ in influencers]
        if influ['email'] not in influencer_emails:

            influencer = db.session.get(Influencer, influ['id'])

            sponsor_names = []
            for ass_ad in influencer.assigned_ads:
                if (ass_ad.status.name == 'Pending') and (ass_ad.campaign.sponsor.name not in sponsor_names):
                    sponsor_names.append(ass_ad.campaign.sponsor.name)

            influ['pending_ads_sponsor_names'] = sponsor_names
            influencers.append(influ)

    # Testing
    # for influencer in influencers:
    #     sponsors = '\n'.join(f'{idx + 1}. ' + sponsor_name for (idx, sponsor_name) in enumerate(influencer['pending_ads_sponsor_names']))
    #     print('---'*30)
    #     print(f"Hi {influencer['name']},\n\nYou have pending ad requests from:\n{sponsors}\n\nPlease visit our website to take action.\nAlso don't forget to check out the Public Campaigns listed on our website.\n\nThanks,\nTeam SponsorConnect")

    return influencers
