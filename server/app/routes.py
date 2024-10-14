from flask import current_app as app, jsonify, request, abort
from flask_security import current_user, auth_required, roles_required, roles_accepted, login_user, logout_user

from app.models import db
from app.models import *

from datetime import date

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

@app.route("/sponsor/campaigns")
@auth_required('token')
@roles_required('Sponsor')
def all_campaigns():
    data = { 'campaigns': [] }
    campaigns = current_user.sponsor.campaigns  # Sponsor Campaigns

    for campaign in campaigns:
        camp = {
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
        }
        data['campaigns'].append(camp)

    return jsonify(data)
    

@app.route('/influencer/campaigns')
@auth_required('token')
@roles_required('Influencer')
def public_campaigns():
    data = { 'campaigns': [] }
    campaigns = db.session.query(Campaign).filter(Campaign.visibility_id == 1).all()  # All Public Campaigns

    for campaign in campaigns:
        camp = {
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
        }
        data['campaigns'].append(camp)

    return jsonify(data)

@app.route('/active-campaigns')
@auth_required("token")
@roles_accepted('Sponsor', 'Influencer')
def active_campaigns():
    data = {
        'campaigns': [], 
    }

    # TODO: Admin can access this.

    if current_user.sponsor:
        for campaign in current_user.sponsor.campaigns:
            camp = {
                'id': campaign.id,
                'name': campaign.name,
                'flagged': campaign.flagged,
                'end_date': campaign.end_date,
                'visibility': campaign.campaign_visibility.name,
                'ad_requests': [],
            }

            for ad_request in campaign.ad_requests:
                ad = {
                    'id': ad_request.id,
                    'requirement': ad_request.requirement,
                    'payment_amount': ad_request.payment_amount,
                    'message': ad_request.message,
                    'status': ad_request.status.name,
                    'sender_user_id': ad_request.sender_user_id,
                    'influencer_id': ad_request.influencer_id,
                }

                camp['ad_requests'].append(ad)
            
            if campaign.end_date > date.today():
                data['campaigns'].append(camp)

        return jsonify(data)
    
    for ad_request in current_user.influencer.assigned_ads:
        campaign = ad_request.campaign
        camp = {
            'id': campaign.id,
            'name': campaign.name,
            'flagged': campaign.flagged,
            'end_date': campaign.end_date,
            'visibility': campaign.campaign_visibility.name,
        }
        camp_ids = [camp['id'] for camp in data['campaigns']]
        if (campaign.end_date > date.today()) and (camp['id'] not in camp_ids):
            data['campaigns'].append(camp)

    return jsonify(data)

@app.route('/pending-ad-requests')
@auth_required("token")
@roles_accepted('Sponsor', 'Influencer')
def pending_ad_requests():
    data = {
        'pending_ad_requests': {
            'sent': [],
            'received': []
        }
    }

    if current_user.sponsor:
        for campaign in current_user.sponsor.campaigns:
            for ad_request in campaign.ad_requests:
                ad = {
                    'id': ad_request.id,
                    'requirement': ad_request.requirement,
                    'payment_amount': ad_request.payment_amount,
                    'message': ad_request.message,
                    'status': ad_request.status.name,
                    'sender_user_id': ad_request.sender_user_id,
                    'influencer_id': ad_request.influencer_id,
                    'influencer_name': ad_request.influencer.name if ad_request.influencer_id else None,
                    'sponsor_name': ad_request.campaign.sponsor.name,
                }

                if (ad_request.status.name == "Pending") and (ad_request.influencer_id) and (not ad_request.campaign.flagged):
                    if ad_request.sender_user_id == current_user.id:
                        data['pending_ad_requests']['sent'].append(ad)
                    else:
                        data['pending_ad_requests']['received'].append(ad)
        
        return jsonify(data)
    
    for ad_request in current_user.influencer.assigned_ads:
        ad = {
            'id': ad_request.id,
            'requirement': ad_request.requirement,
            'payment_amount': ad_request.payment_amount,
            'message': ad_request.message,
            'status': ad_request.status.name,
            'sender_user_id': ad_request.sender_user_id,
            'influencer_id': ad_request.influencer_id,
            'influencer_name': ad_request.influencer.name if ad_request.influencer_id else None,
            'sponsor_name': ad_request.campaign.sponsor.name,
        }

        if (ad_request.status.name == "Pending") and (not ad_request.campaign.flagged):
            if ad_request.sender_user_id == current_user.id:
                data['pending_ad_requests']['sent'].append(ad)
            else:
                data['pending_ad_requests']['received'].append(ad)
    
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


@app.route("/ad-request/<int:ad_request_id>/accept")
@auth_required("token")
@roles_accepted('Sponsor', 'Influencer')
def accept_ad_request(ad_request_id):
    ad_request = db.session.get(AdRequest, ad_request_id)

    # if not ad_request:
    #     abort(404, description="Ad request not found.")

    # if ad_request.sender_user_id == current_user.id:
    #     abort(405, description="You cannot accept your own ad request.")

    # if ad_request.status.name != "Pending":
    #     abort(405, description="You cannot accept this request.")
    
    # if ad_request.campaign.flagged:
    #     abort(405, description="Campaign is flagged by the admin.")
    
    # if current_user.influencer:
    #     if ad_request.influencer == None:
    #         ad_request.influencer = current_user.influencer
    #     else:
    #         if ad_request.influencer_id != current_user.influencer.id:
    #             abort(405, description="Ad request is not assigned to you.")
    
    # if current_user.sponsor:
    #     if ad_request.campaign.sponsor.id != current_user.sponsor.id:
    #         abort(405, description="Ad request does not belong to your campaign.")

    ad_request.status_id = 2  # Accepted
    db.session.commit()

    return jsonify({ 'message': 'Successfully accepted ad request.' })


@app.route("/ad-request/<int:ad_request_id>/reject")
@auth_required("token")
@roles_accepted('Sponsor', 'Influencer')
def reject_ad_request(ad_request_id):
    ad_request = db.session.get(AdRequest, ad_request_id)

    # if not ad_request:
    #     abort(404, description="Ad request not found.")

    # if ad_request.sender_user_id == current_user.id:
    #     abort(403, description="You cannot reject your own ad Request!")
    
    # if ad_request.status.name != "Pending":
    #     abort(403, description="You cannot reject this ad request.")
    
    # if ad_request.campaign.flagged:
    #     abort(403, description="Campaign is flagged by the admin.")
    
    # if ad_request.influencer == None:
    #     abort(405, description="You cannot reject this ad request.")
    
    # if current_user.influencer:
    #     if ad_request.influencer_id != current_user.influencer.id:
    #         abort(405, description="Ad request is not assigned to you.")
    
    # if current_user.sponsor:
    #     if ad_request.campaign.sponsor.id != current_user.sponsor.id:
    #         abort(405, description="Ad request does not belong to your campaign.")
    
    ad_request.status_id = 3
    db.session.commit()

    return jsonify({ 'message': 'Successfully rejected ad request.' })

@app.route("/ad-request/<int:ad_request_id>/negotiate", methods=["POST"])
@auth_required("token")
@roles_accepted('Sponsor', 'Influencer')
def negotiate_ad_request(ad_request_id):
    content = request.json
    ad_request = db.session.get(AdRequest, ad_request_id)

    if ad_request.influencer == None:
        ad_request.influencer = current_user.influencer

    try:
        payment_amount = float(content.get("payment_amount", 0))
    except (ValueError, TypeError) as e:
        # logging.error(f"Error converting payment_amount to float: {e}")
        payment_amount = 0
    
    if payment_amount < 0:
        abort(405, description="Payment amount cannot be negative.")
    
    campaign_budget = ad_request.campaign.budget + ad_request.payment_amount
    if payment_amount > campaign_budget:
        abort(405, description="Payment Amount cannot be greater than the Campaign Budget.")
    
    ad_request.campaign.budget = campaign_budget - payment_amount
    
    ad_request.payment_amount = payment_amount
    ad_request.message = content.get("message", None)
    ad_request.requirement = content.get("requirement", None)
    ad_request.sender_user_id = current_user.id

    db.session.commit()

    return jsonify({ 'message': 'Successfully negotiated ad request.' })
