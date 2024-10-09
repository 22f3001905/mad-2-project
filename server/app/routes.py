from flask import current_app as app, jsonify, request
from flask_security import current_user, auth_required, roles_required, roles_accepted, login_user, logout_user

from app.models import db
from app.models import *

# @roles_required("Student", "Instructor") -> User should have both Student and Instructor. { AND condition }
# @roles_accepted("Student", "Instructor") -> User should have either Student or Instructor. { OR condition }

@app.route("/info/user")
@auth_required("token")
def user_info():
    # current_user: Proxy of the logged in user. Comes from the Session.
    info = {
        "id": current_user.id,
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
            'goals': [{ 'id': goal.id, 'name': goal.name, 'status': goal.status } for goal in campaign.goals],
            'n_ads': len(campaign.ad_requests),
            'n_unassigned_ads': len([ad for ad in campaign.ad_requests if not ad.influencer_id])
        })
    return jsonify(data)

@app.route("/info/influencer")
@auth_required("token")
@roles_required("Influencer")
def influencer_info():
    if current_user.influencer == None:
        return jsonify({ 'message': 'Influencer not found.' }), 404
    
    assigned_ads = []

    for ad_request in current_user.influencer.assigned_ads:
        ad = {
            'id': ad_request.id,
            'requirement': ad_request.requirement,
            'payment_amount': ad_request.payment_amount,
            'message': ad_request.message,
            'status': ad_request.status.name,
            'sender_user_id': ad_request.sender_user_id,
        }
        assigned_ads.append(ad)
    
    info = {
        "name": current_user.influencer.name,
        "category": current_user.influencer.category.name,
        "niche": current_user.influencer.niche,
        "reach": current_user.influencer.reach,
        "wallet_balance": current_user.influencer.wallet_balance,
        "assigned_ads": assigned_ads
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


@app.route('/influencer/<int:influencer_id>')
def influencer_details(influencer_id):
    influencer = db.session.get(Influencer, influencer_id)
    influencer_out = {
        'id': influencer.id,
        'name': influencer.name,
    }
    return jsonify({ 'influencer': influencer_out })


# @app.route('/unassigned-ads')
# def ads_unassigned():
#     pass

@app.route('/assign-ad', methods=['POST'])
@auth_required("token")
@roles_accepted('Sponsor', 'Influencer')
def ad_assign():
    content = request.json
    print(content)
    
    ad_request = db.session.get(AdRequest, content['ad_request_id'])
    ad_request.influencer_id = content['influencer_id']

    db.session.commit()

    return jsonify({ 'message': 'Successfully assigned ad request.' })
