from flask import current_app as app
from flask_security import hash_password

def create_user(email, password, roles: list):
    user_exists = app.security.datastore.find_user(email=email)
    if not user_exists:
        hashed_password = hash_password(password)
        app.security.datastore.create_user(email=email, password=hashed_password, roles=roles)
        return app.security.datastore.find_user(email=email)

def hard_coded_info():
    industry_names = ['Fashion/Apparel', 'Food & Beverage', 'Beauty/Cosmetics', 'Travel', 'Health/Fitness', 'Technology', 'Entertainment', 'Automotive', 'Education', 'Other']
    influencer_category_names = ['Fashion', 'Fitness', 'Travel', 'Food', 'Tech', 'Lifestyle', 'Education', 'Gaming', 'Finance', 'Other']
    campaign_niche_names = ['Social Media Advertising', 'Video Advertising', 'Sponsored Content', 'Affiliate Marketing', 'Sponsored Posts', 'Other']

    return {
        "industry_names": industry_names, 
        "influencer_category_names": influencer_category_names, 
        "campaign_niche_names": campaign_niche_names
    }

from app.models import *

def basic_setup():
    visi_names = ("Public", "Private")
    visis = []

    for visi_name in visi_names:
        visis.append(CampaignVisibility(name=visi_name))

    status_names = ('Pending', 'Accepted', 'Rejected', 'Completed')
    stati = []

    for status_name in status_names:
        stati.append(Status(name=status_name))

    industry_names = ('Fashion/Apparel', 'Food & Beverage', 'Beauty/Cosmetics', 'Travel', 'Health/Fitness', 'Technology', 'Entertainment', 'Automotive', 'Education', 'Other')
    industries = []

    for industry_name in industry_names:
        industries.append(Industry(name=industry_name))
    
    influencer_category_names = ('Fashion', 'Fitness', 'Travel', 'Food', 'Tech', 'Lifestyle', 'Education', 'Gaming', 'Finance', 'Other')
    influencer_categories = []

    for influencer_category_name in influencer_category_names:
        influencer_categories.append(InfluencerCategory(name=influencer_category_name))
    
    campaign_niche_names = ('Social Media Advertising', 'Video Advertising', 'Sponsored Content', 'Affiliate Marketing', 'Sponsored Posts', 'Other')
    campaign_niches = []

    for niche_name in campaign_niche_names:
        campaign_niches.append(CampaignNiche(name=niche_name))
    
    db.session.add_all(visis)
    db.session.add_all(stati)
    db.session.add_all(industries)
    db.session.add_all(influencer_categories)
    db.session.add_all(campaign_niches)
    db.session.commit()
