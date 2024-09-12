from flask import current_app as app
from flask_security import hash_password

def create_user(email, password, roles: list):
    user_exists = app.security.datastore.find_user(email=email)
    if not user_exists:
        hashed_password = hash_password(password)
        app.security.datastore.create_user(email=email, password=hashed_password, roles=roles)

def hard_coded_info():
    industry_names = ['Fashion/Apparel', 'Food & Beverage', 'Beauty/Cosmetics', 'Travel', 'Health/Fitness', 'Technology', 'Entertainment', 'Automotive', 'Education', 'Other']
    influencer_category_names = ['Fashion', 'Fitness', 'Travel', 'Food', 'Tech', 'Lifestyle', 'Education', 'Gaming', 'Finance', 'Other']
    campaign_niche_names = ['Social Media Advertising', 'Video Advertising', 'Sponsored Content', 'Affiliate Marketing', 'Sponsored Posts', 'Other']

    return {
        "industry_names": industry_names, 
        "influencer_category_names": influencer_category_names, 
        "campaign_niche_names": campaign_niche_names
    }
