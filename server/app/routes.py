from flask import current_app as app, jsonify, request, abort,send_file
from flask_security import current_user, auth_required, roles_required, roles_accepted, login_user, logout_user

from app.models import db
from app.models import *

from datetime import date
from app.utils import not_flagged, not_approved, user_specific_key
from app.cache import cache

# @roles_required { AND condition }
# @roles_accepted { OR condition }

@app.route("/info/user")
@auth_required("token")
@cache.cached(60, key_prefix=lambda: user_specific_key('info'))
def user_info():
    # current_user: Proxy of the logged in user. Comes from the Session.
    user_roles = [role.name for role in current_user.roles]
    
    info = {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.roles[0].name if 'Admin' not in user_roles else 'Admin',
        "name": current_user.sponsor.name if current_user.sponsor else current_user.influencer.name if current_user.influencer else 'Admin'
    }
    return jsonify(info)

@app.route("/info/sponsor")
@auth_required("token")
@roles_required("Sponsor")
@not_flagged()
@not_approved()
@cache.cached(60, key_prefix=lambda: user_specific_key('sponsor_info'))
def sponsor_info():
    if current_user.sponsor == None:
        user_id = request.args.get('userId')
        if not user_id:
            return jsonify({ 'message': 'Sponsor not found.' }), 404
        user = db.session.get(User, user_id)
        sponsor = user.sponsor
    else:
        sponsor = current_user.sponsor
    
    campaigns = []
    for campaign in sponsor.campaigns:
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
        "name": sponsor.name,
        "industry": sponsor.industry.name,
        "budget": sponsor.budget,
        "campaigns": campaigns
    }

    return jsonify(info)

@app.route("/sponsor/campaigns")
@auth_required('token')
@roles_required('Sponsor')
@not_flagged()
@not_approved()
@cache.cached(60, key_prefix=lambda: user_specific_key('campaigns'))
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
@not_flagged()
@cache.cached(60, key_prefix=lambda: user_specific_key('public_campaigns'))
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
@roles_accepted('Sponsor', 'Influencer', 'Admin')
@not_flagged()
@not_approved()
@cache.cached(60, key_prefix=lambda: user_specific_key('active_campaigns'))
def active_campaigns():
    data = {
        'campaigns': [], 
    }

    if current_user.sponsor or current_user.id == 1:
        if current_user.id == 1:
            campaigns = db.session.query(Campaign).all()
        else:
            campaigns = current_user.sponsor.campaigns
        
        for campaign in campaigns:
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
@not_flagged()
@not_approved()
@cache.cached(60, key_prefix=lambda: user_specific_key('pending_requests'))
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
@not_flagged()
@cache.cached(60, key_prefix=lambda: user_specific_key('influencer_info'))
def influencer_info():
    if current_user.influencer == None:
        user_id = request.args.get('userId')
        if not user_id:
            return jsonify({ 'message': 'Influencer not found.' }), 404
        user = db.session.get(User, user_id)
        influencer = user.influencer
    else:
        influencer = current_user.influencer
    
    assigned_ads = []

    for ad_request in influencer.assigned_ads:
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
        "name": influencer.name,
        "category": influencer.category.name,
        "niche": influencer.niche,
        "reach": influencer.reach,
        "wallet_balance": influencer.wallet_balance,
        "assigned_ads": assigned_ads
    }

    return jsonify(info)

from app.utils import form_hard_coded

@app.route("/hard-coded-form-data")
# @cache.cached(60, key_prefix=lambda: user_specific_key('hard_coded_form_data'))
@cache.cached(60)
def registration_form_data():
    return jsonify(form_hard_coded())

@app.route('/sponsor-budget')
@auth_required("token")
@roles_required("Sponsor")
@not_flagged()
@not_approved()
@cache.cached(60, key_prefix=lambda: user_specific_key('sponsor_budget'))
def sponsor_budget():
    budget = current_user.sponsor.budget
    return jsonify({ 'budget': budget })


@app.route('/influencer/<int:influencer_id>')
# @cache.cached(timeout=60, key_prefix=lambda: user_specific_key(f"influencer_{request.view_args['influencer_id']}"))
def influencer_details(influencer_id):
    influencer = db.session.get(Influencer, influencer_id)
    influencer_out = {
        'id': influencer.id,
        'name': influencer.name,
    }
    return jsonify({ 'influencer': influencer_out })


@app.route('/search/users', methods=['POST'])
@auth_required("token")
@roles_accepted('Admin')
def search_users():
    content = request.json
    keyword = content.get('keyword')

    users = db.session.query(User).filter((User.id != 1)).all()
    out = []
    for user in users:
        if user.sponsor:
            out.append({
                'user_id': user.id,
                'email': user.email,
                'role': 'Sponsor',
                'flagged': user.flagged,
                'id': user.sponsor.id,
                'name': user.sponsor.name,
                'wallet': user.sponsor.budget,
            })
        else:
            out.append({
                'user_id': user.id,
                'email': user.email,
                'role': 'Influencer',
                'flagged': user.flagged,
                'id': user.influencer.id,
                'name': user.influencer.name,
                'wallet': user.influencer.wallet_balance,
            })
    
    if keyword:
        keyword = keyword.strip().lower()
        out = [user for user in out if (keyword in user['name'].lower()) or (keyword in user['email'].lower())]
    
    return jsonify({ 'data': out })

@app.route('/user/<int:user_id>')
@auth_required("token")
@roles_accepted('Admin')
def user_profile(user_id):
    user = db.session.get(User, user_id)

    if user.sponsor:
        user_info = {
            'user_id': user.id,
            'email': user.email,
            'role': 'Sponsor',
            'flagged': user.flagged,
            'id': user.sponsor.id,
            'name': user.sponsor.name,
            'wallet': user.sponsor.budget,
        }

        return jsonify({ 'data': user_info })

    user_info = {
        'user_id': user.id,
        'email': user.email,
        'role': 'Influencer',
        'flagged': user.flagged,
        'id': user.influencer.id,
        'name': user.influencer.name,
        'wallet': user.influencer.wallet_balance,
    }
    
    return jsonify({ 'data': user_info })


@app.route('/assign-ad', methods=['POST'])
@auth_required("token")
@roles_accepted('Sponsor', 'Influencer')
@not_flagged()
@not_approved()
def ad_assign():
    content = request.json

    ad_request = db.session.get(AdRequest, content['ad_request_id'])
    ad_request.influencer_id = content['influencer_id']

    db.session.commit()

    return jsonify({ 'message': 'Successfully assigned ad request.' })


@app.route("/ad-request/<int:ad_request_id>/accept")
@auth_required("token")
@roles_accepted('Sponsor', 'Influencer')
@not_flagged()
@not_approved()
def accept_ad_request(ad_request_id):
    ad_request = db.session.get(AdRequest, ad_request_id)

    if not ad_request:
        abort(404, description="Ad request not found.")

    if ad_request.sender_user_id == current_user.id:
        abort(405, description="You cannot accept your own ad request.")

    if ad_request.status.name != "Pending":
        abort(405, description="You cannot accept this request.")
    
    if ad_request.campaign.flagged:
        abort(405, description="Campaign is flagged by the admin.")
    
    if current_user.influencer:
        if ad_request.influencer == None:
            ad_request.influencer = current_user.influencer
        else:
            if ad_request.influencer_id != current_user.influencer.id:
                abort(405, description="Ad request is not assigned to you.")
    
    if current_user.sponsor:
        if ad_request.campaign.sponsor.id != current_user.sponsor.id:
            abort(405, description="Ad request does not belong to your campaign.")

    ad_request.status_id = 2  # Accepted
    db.session.commit()

    return jsonify({ 'message': 'Successfully accepted ad request.' })


@app.route("/ad-request/<int:ad_request_id>/reject")
@auth_required("token")
@roles_accepted('Sponsor', 'Influencer')
@not_flagged()
@not_approved()
def reject_ad_request(ad_request_id):
    ad_request = db.session.get(AdRequest, ad_request_id)

    if not ad_request:
        abort(404, description="Ad request not found.")

    if ad_request.sender_user_id == current_user.id:
        abort(403, description="You cannot reject your own ad Request!")
    
    if ad_request.status.name != "Pending":
        abort(403, description="You cannot reject this ad request.")
    
    if ad_request.campaign.flagged:
        abort(403, description="Campaign is flagged by the admin.")
    
    if ad_request.influencer == None:
        abort(405, description="You cannot reject this ad request.")
    
    if current_user.influencer:
        if ad_request.influencer_id != current_user.influencer.id:
            abort(405, description="Ad request is not assigned to you.")
    
    if current_user.sponsor:
        if ad_request.campaign.sponsor.id != current_user.sponsor.id:
            abort(405, description="Ad request does not belong to your campaign.")
    
    ad_request.status_id = 3
    db.session.commit()

    return jsonify({ 'message': 'Successfully rejected ad request.' })

@app.route("/ad-request/<int:ad_request_id>/negotiate", methods=["POST"])
@auth_required("token")
@roles_accepted('Sponsor', 'Influencer')
@not_flagged()
@not_approved()
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

@app.route("/ad-request/<int:ad_request_id>/complete")
@auth_required("token")
@roles_required('Influencer')
@not_flagged()
def complete_ad_request(ad_request_id):
    ad_request = db.session.get(AdRequest, ad_request_id)

    if not ad_request:
        abort(404, description="Ad request not found.")

    is_assigned_ad = ad_request in current_user.influencer.assigned_ads
    
    if (not is_assigned_ad) or (ad_request.status.name != "Accepted"):
        abort(405, description="You're not allowed to complete this ad request.")
    
    ad_request.status_id = 4
    ad_request.influencer.wallet_balance += ad_request.payment_amount
    
    db.session.commit()

    return jsonify({ 'message': 'Successfully completed ad request.' })


@app.route("/influencer/stats")
@auth_required("token")
@roles_required('Influencer')
@not_flagged()
@cache.cached(timeout=60, key_prefix=lambda: user_specific_key("influencer_stats"))
def stats_influencer():
    influencer = current_user.influencer
    monthly_ad_revenue = [0 for _ in range(12)]
    ad_request_initialize = {"sent": 0, "received": 0}

    statuses = [status.name for status in db.session.query(Status).all()]
    ad_request_status = { status: 0 for status in statuses }

    for ad_request in influencer.assigned_ads:
        ad_request_status[ad_request.status.name] += 1

        if ad_request.sender_user_id == influencer.user.id:
            ad_request_initialize["sent"] += 1
        else:
            ad_request_initialize["received"] += 1

        if ad_request.status.name not in ("Rejected"):
            monthly_ad_revenue[ad_request.campaign.end_date.month - 1] += ad_request.payment_amount

    data = dict(
        monthly_ad_revenue=monthly_ad_revenue, 
        ad_request_initialize=ad_request_initialize, 
        ad_request_status=ad_request_status, 
    )

    return jsonify(data)

@app.route("/sponsor/stats")
@auth_required("token")
@roles_required('Sponsor')
@not_flagged()
@not_approved()
@cache.cached(timeout=60, key_prefix=lambda: user_specific_key("sponsor_stats"))
def stats_sponsor():
    sponsor = current_user.sponsor
    
    statuses = [status.name for status in db.session.query(Status).all()]
    ad_request_status = { status: 0 for status in statuses }
    ad_request_payout_agg = { status: 0 for status in statuses }
    ad_request_payout = []

    campaigns = [
        {
            'name': 'Unallocated',
            'budget': sponsor.budget
        }
    ]
    for campaign in sponsor.campaigns:

        payout_by_status = { status: 0 for status in statuses }
        
        for ad_request in campaign.ad_requests:
            ad_request_status[ad_request.status.name] += 1

            ad_request_payout_agg[ad_request.status.name] += ad_request.payment_amount
            payout_by_status[ad_request.status.name] += ad_request.payment_amount

        payout_by_status['campaign_name'] = campaign.name
        
        ad_request_payout.append(payout_by_status)
        
        campaigns.append({
            'name': campaign.name,
            'budget': campaign.budget,
        })
    
    data = dict(
        ad_request_status=ad_request_status, 
        campaigns=campaigns, 
        ad_request_payout=ad_request_payout,
        ad_request_payout_agg=ad_request_payout_agg,
    )

    return jsonify(data)

@app.route('/admin/stats')
@auth_required("token")
@roles_required('Admin')
@cache.cached(timeout=60, key_prefix=lambda: user_specific_key("admin_stats"))
def stats_admin():
    users = db.session.query(User).all()
    active_users = {
        'Sponsor': 0,
        'Influencer': 0,
        'Flagged': 0
    }
    for user in users:
        if user.flagged:
            active_users['Flagged'] += 1
        else:
            if user.sponsor:
                active_users['Sponsor'] += 1
            elif user.influencer:
                active_users['Influencer'] += 1

    campaigns = db.session.query(Campaign).all()
    campaigns_info = {
        'Public': 0,
        'Private': 0,
        'Flagged': 0
    }
    monthly_campaigns = [0 for _ in range(12)]
    for campaign in campaigns:
        monthly_campaigns[campaign.start_date.month - 1] += 1
        
        if campaign.flagged:
            campaigns_info['Flagged'] += 1
        else:
            if campaign.campaign_visibility.name == 'Public':
                campaigns_info['Public'] += 1
            else:
                campaigns_info['Private'] += 1

    ad_request_statuses = { status.name: 0 for status in db.session.query(Status).all() }
    monthly_ad_request_payments = [0 for _ in range(12)]

    ad_requests = db.session.query(AdRequest).all()
    for ad in ad_requests:
        ad_request_statuses[ad.status.name] += 1
        if ad.status.name == "Completed":
            monthly_ad_request_payments[ad.campaign.end_date.month - 1] += (ad.payment_amount * 0.05)

    data = dict(
        active_users=active_users,
        campaigns_info=campaigns_info,
        monthly_campaigns=monthly_campaigns,
        ad_request_statuses=ad_request_statuses,
        monthly_ad_request_payments=monthly_ad_request_payments
    )

    return jsonify(data)


from app.tasks import export_campaigns_data

@app.route('/campaigns/download')
@auth_required("token")
@roles_required('Sponsor')
@not_flagged()
@not_approved()
def download_campaigns():
    campaigns = []
    for camp in current_user.sponsor.campaigns:
        goals_achieved = []
        for ad in camp.ad_requests:
            if ad.status.name == 'Completed':
                if ad.campaign_goal.name not in goals_achieved:
                    goals_achieved.append(ad.campaign_goal.name)
        
        campaigns.append({
            'name': camp.name,
            'start_date': camp.start_date.strftime("%Y-%m-%d"),
            'end_date': camp.end_date.strftime("%Y-%m-%d"),
            'budget': camp.budget,
            'goals': [goal.name for goal in camp.goals],
            'goals_achieved': goals_achieved,
            'n_goals_achieved': len(goals_achieved),
            'n_ads': len(camp.ad_requests),
            'completed_ads': len([ad for ad in camp.ad_requests if ad.status.name == 'Completed'])
        })
    
    task = export_campaigns_data.delay(campaigns, current_user.sponsor.name)
    return jsonify({ 'message': 'Your .csv file is being generated.', 'task_id': task.id })

from celery.result import AsyncResult

# Used to poll the pending task.
@app.route("/exports/<task_id>")
@auth_required("token")
@roles_required('Sponsor')
@not_flagged()
@not_approved()
def task_exports(task_id):
    result = AsyncResult(id=task_id)
    output = {
        "id": result.id,
        "ready": result.ready(),
        "status": result.status,
        "value": result.result if result.ready() else None
    }

    return jsonify(output)

@app.route('/campaigns/download/<path:file_path>')
@auth_required("token")
@roles_required('Sponsor')
@not_flagged()
@not_approved()
def download_csv(file_path):
    response = send_file(file_path, as_attachment=True)
    # os.remove(file_path)
    return response

@app.route("/user/<int:user_id>/flag")
@auth_required("token")
@roles_required('Admin')
def flag_user(user_id):
    user = db.session.get(User, user_id)

    if not user:
        abort(404, description="User not found!")
    
    if user.flagged:
        abort(403, description="User is already flagged.")

    user.flagged = True
    db.session.commit()

    return jsonify({ 'message': 'User was flagged successfully.' })

@app.route("/user/<int:user_id>/unflag")
@auth_required("token")
@roles_required('Admin')
def unflag_user(user_id):
    user = db.session.get(User, user_id)

    if not user:
        abort(404, description="User not found!")
    
    if not user.flagged:
        abort(403, description="User is not flagged.")

    user.flagged = False
    db.session.commit()

    return jsonify({ 'message': 'User was unflagged successfully.' })


@app.route("/campaign/<int:campaign_id>/flag")
@auth_required("token")
@roles_required('Admin')
def flag_campaign(campaign_id):
    campaign = db.session.get(Campaign, campaign_id)
    if not campaign:
        abort(404, description="Campaign not found!")
    
    if campaign.flagged:
        abort(403, description="Campaign is already flagged.")

    campaign.flagged = True
    db.session.commit()

    return jsonify({ 'message': 'Campaign was flagged successfully.' })

@app.route("/campaign/<int:campaign_id>/unflag")
@auth_required("token")
@roles_required('Admin')
def unflag_campaign(campaign_id):
    campaign = db.session.get(Campaign, campaign_id)
    if not campaign:
        abort(404, description="Campaign not found!")
    
    if not campaign.flagged:
        abort(403, description="Campaign is not flagged.")

    campaign.flagged = False
    db.session.commit()

    return jsonify({ 'message': 'Campaign was unflagged successfully.' })

from app.utils import get_sponsors

@app.route("/sponsors-approval-pending")
@auth_required("token")
@roles_required('Admin')
def pending_approval_sponsors():
    sponsors = get_sponsors()
    approval_pending_sponsors = [sponsor for sponsor in sponsors if not sponsor['approved']]
    return jsonify({ 'data': approval_pending_sponsors })


@app.route("/sponsor-approval/<int:sponsor_id>")
@auth_required("token")
@roles_required('Admin')
def approve_sponsor(sponsor_id):
    sponsor = db.session.get(Sponsor, sponsor_id)

    if not sponsor:
        abort(404, description='Sponsor not found!')
    if sponsor.approved:
        abort(403, description='Sponsor is already approved.')
    
    sponsor.approved = True

    db.session.commit()
    return jsonify({ 'message': 'Sponsor was approved.' })
