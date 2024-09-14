from flask import current_app as app, jsonify
from flask_security import current_user, auth_required, roles_required, roles_accepted, login_user, logout_user

from app.utils import hard_coded_info

# @roles_required("Student", "Instructor") -> User should have both Student and Instructor. { AND condition }
# @roles_accepted("Student", "Instructor") -> User should have either Student or Instructor. { OR condition }

@app.route("/user/info")
@auth_required("token")
def user_info():
    # current_user: Proxy of the logged in user. Comes from the Session.
    info = {
        "email": current_user.email,
        "role": current_user.roles[0].name
    }
    return jsonify(info)

@app.route("/sponsor/info")
@auth_required("token")
@roles_required("Sponsor")
def sponsor_info():
    if current_user.sponsor == None:
        return jsonify({  })
    info = {
        "name": current_user.sponsor.name,
        "industry": current_user.sponsor.industry.name,
        "budget": current_user.sponsor.budget,
        "campaigns": current_user.sponsor.campaigns
    }
    return jsonify(info)

@app.route("/influencer/info")
@auth_required("token")
@roles_required("Influencer")
def influencer_info():
    if current_user.influencer == None:
        return jsonify({  })
    info = {
        "name": current_user.influencer.name,
        "category": current_user.influencer.category.name,
        "niche": current_user.influencer.niche,
        "reach": current_user.influencer.reach,
        "wallet_balance": current_user.influencer.wallet_balance,
        "assigned_ads": current_user.influencer.assigned_ads
    }
    return jsonify(info)

@app.route("/registration-form-data")
def registration_form_data():
    return jsonify(hard_coded_info())
