from flask import current_app as app, jsonify
from flask_security import current_user, auth_required, roles_required, roles_accepted, login_user, logout_user

# @roles_required("Student", "Instructor") -> User should have both Student and Instructor. { AND condition }
# @roles_accepted("Student", "Instructor") -> User should have either Student or Instructor. { OR condition }

@app.route("/info/user")
@auth_required("token")
def user_info():
    # current_user: Proxy of the logged in user. Comes from the Session.
    info = {
        "email": current_user.email,
        "role": current_user.roles[0].name
    }
    return jsonify(info)

@app.route("/info/sponsor")
@auth_required("token")
@roles_required("Sponsor")
def sponsor_info():
    if current_user.sponsor == None:
        return jsonify({ 'message': 'Sponsor not found.' }), 404
    
    campaigns = []
    for campaign in current_user.sponsor.campaigns:
        campaigns.append({
            'id': campaign.id,
            'name': campaign.name,
            # 'description': campaign.description,
            # 'start_date': campaign.start_date,
            'end_date': campaign.end_date,
            # 'budget': campaign.budget,
            'visibility': campaign.campaign_visibility.name,
            # 'niche': campaign.niche.name,
            # 'ad_requests': campaign.ad_requests,
            # 'goals': [{ 'name': goal.name, 'status': goal.status } for goal in campaign.goals],
            'flagged': campaign.flagged
        })
    
    info = {
        "name": current_user.sponsor.name,
        "industry": current_user.sponsor.industry.name,
        "budget": current_user.sponsor.budget,
        "campaigns": campaigns
    }

    return jsonify(info)

@app.route("/all-campaigns")
@auth_required('token')
@roles_required("Sponsor")
def all_campaigns():
    data = {
        'campaigns': []
    }
    for campaign in current_user.sponsor.campaigns:
        data['campaigns'].append({
            'id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'start_date': campaign.start_date,
            'end_date': campaign.end_date,
            'budget': campaign.budget,
            'visibility': campaign.campaign_visibility.name,
            'niche': campaign.niche.name,
            'flagged': campaign.flagged,
            'goals': [{ 'id': goal.id, 'name': goal.name, 'status': goal.status } for goal in campaign.goals]
        })
    return jsonify(data)

@app.route("/info/influencer")
@auth_required("token")
@roles_required("Influencer")
def influencer_info():
    if current_user.influencer == None:
        return jsonify({ 'message': 'Influencer not found.' }), 404
    
    info = {
        "name": current_user.influencer.name,
        "category": current_user.influencer.category.name,
        "niche": current_user.influencer.niche,
        "reach": current_user.influencer.reach,
        "wallet_balance": current_user.influencer.wallet_balance,
        "assigned_ads": current_user.influencer.assigned_ads
    }

    return jsonify(info)

from app.utils import form_hard_coded

@app.route("/hard-coded-form-data")
def registration_form_data():
    return jsonify(form_hard_coded())

@app.route('/sponsor-budget')
@auth_required("token")
@roles_required("Sponsor")
def sponsor_budget():
    budget = current_user.sponsor.budget
    return jsonify({ 'budget': budget })
