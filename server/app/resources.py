from flask import current_app as app, abort
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_security import auth_required, roles_required, current_user, roles_accepted

from app.utils import create_user, not_flagged, not_approved
from app.models import db
from app.models import *
from app.validation import *

from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

import logging

api = Api()

user_parser = reqparse.RequestParser()
user_parser.add_argument("email")
user_parser.add_argument("password")
user_parser.add_argument("roles", type=str, action="append")  # roles: list

user_parser.add_argument("companyName")
user_parser.add_argument("industryId", type=int)

user_parser.add_argument("influencerName")
user_parser.add_argument("categoryId", type=int)
user_parser.add_argument("niche")
user_parser.add_argument("reach", type=int)

class UserAPI(Resource):
    def post(self):
        user_args = user_parser.parse_args()
        email = user_args.get("email")
        password = user_args.get("password")
        roles = user_args.get("roles")

        user = create_user(email, password, roles)
        if user == None:
            return { "message": "User cannot be created." }, 402

        # Needs ADMIN Approval
        if roles[0] == "Sponsor":
            company_name = user_args.get("companyName")
            industry_id = user_args.get("industryId")
            sponsor = Sponsor(
                name=company_name,
                industry_id=industry_id,
                user=user,
                approved=False
            )
            db.session.add(sponsor)
            db.session.commit()
            return {"message": "User waiting to be approved by the admin."}, 201
        
        influencer_name = user_args.get("influencerName")
        category_id = user_args.get("categoryId")
        niche = user_args.get("niche")
        reach = user_args.get("reach")
        influencer = Influencer(
            name=influencer_name,
            category_id=category_id,
            niche=niche,
            reach=reach,
            user=user
        )
        db.session.add(influencer)
        db.session.commit()

        return { "message": "User created successfully." }, 201


api.add_resource(UserAPI, "/user/create")

influencer_fields = {
    'id': fields.Integer,
    'name': fields.String
}
ad_fields = {
    'id': fields.Integer,
    'requirement': fields.String,
    'payment_amount': fields.Float,
    'message': fields.String,
    'status': fields.String,
    'sender_user_id': fields.Integer,
    'influencer': fields.Nested(influencer_fields)
}
goal_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'status': fields.String,
    'n_ads': fields.Integer
}
niche_fields = {
    'id': fields.Integer,
    'name': fields.String
}
visibility_fields = {
    'id': fields.Integer,
    'name': fields.String
}
campaign_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "start_date": fields.DateTime(dt_format="iso8601"),
    "end_date": fields.DateTime(dt_format="iso8601"),
    "budget": fields.Float,
    "niche": fields.Nested(niche_fields),
    "visibility": fields.Nested(visibility_fields),
    "ad_requests": fields.List(fields.Nested(ad_fields)),
    "goals": fields.List(fields.Nested(goal_fields)),
    "flagged": fields.Boolean
}

campaign_parser = reqparse.RequestParser()
campaign_parser.add_argument("name", type=str)
campaign_parser.add_argument("description", type=str)
campaign_parser.add_argument("start_date", type=str)
campaign_parser.add_argument("end_date", type=str)
campaign_parser.add_argument("niche_id", type=int)
campaign_parser.add_argument("budget", type=float)
campaign_parser.add_argument("visibility_id", type=int)
campaign_parser.add_argument("goals", type=str)

class CampaignAPI(Resource):
    @auth_required('token')
    @roles_required('Sponsor')
    @not_flagged()
    @not_approved()
    def post(self):
        campaign_args = campaign_parser.parse_args()
        name = campaign_args.get("name")
        description = campaign_args.get("description")
        budget = campaign_args.get("budget")
        visibility_id = campaign_args.get("visibility_id")
        goals = campaign_args.get("goals")
        niche_id = campaign_args.get("niche_id")
        start_date = campaign_args.get("start_date")
        end_date = campaign_args.get("end_date")

        if not budget:
            budget = 0

        if budget < 0:
            raise BusinessValidationError(
                status_code=403,
                error_message="Campaign budget cannot be less than 0."
            )

        if not (name and start_date and end_date and visibility_id and niche_id and goals):
            raise IncompleteDataProvidedError()
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        goals = [goal.strip() for goal in goals.strip().split("\n") if goal.strip()]

        if len(goals) == 0:
            raise IncompleteDataProvidedError()

        sponsor = current_user.sponsor
        if not sponsor:
            raise NotFoundError(error_message="Sponsor not found.")

        if start_date > end_date:
            raise BusinessValidationError(
                status_code=403, 
                error_message="End date cannot be before start date."
            )
        
        total_budget = sponsor.budget
        if budget > total_budget:
            raise BusinessValidationError(
                status_code=403, 
                error_message="Campaign budget cannot be greater than total budget."
            )

        sponsor.budget = total_budget - budget

        campaign = Campaign(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            niche_id=niche_id,
            budget=budget,
            visibility_id=visibility_id,
            sponsor=sponsor
        )

        try:
            db.session.add(campaign)

            for goal in goals:
                campaign_goal = CampaignGoal(
                    name=goal,
                    campaign=campaign
                )

                db.session.add(campaign_goal)
            
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            logging.error(f"Database error: {error}")
            raise BusinessValidationError(
                status_code=500,
                error_message="Database error."
            )
        
        return { 'message': 'Campaign created successfully.', 'id': campaign.id }
    
    @auth_required('token')
    @roles_accepted('Sponsor', 'Influencer', 'Admin')
    @marshal_with(campaign_fields)
    def get(self, campaign_id):
        campaign = db.session.get(Campaign, campaign_id)
        
        if not campaign:
            raise NotFoundError(error_message="Campaign not found.")
        
        if current_user.influencer:
            if campaign.campaign_visibility.name == 'Private' and current_user.influencer.id not in [ad.influencer_id for ad in campaign.ad_requests]:
                raise BusinessValidationError(
                    status_code=403, 
                    error_message="Private campaign cannot be viewed by an influencer which is not assigned by sponsor."
                )

        if current_user.sponsor:
            sponsor_id = current_user.sponsor.id
            if campaign.sponsor_id != sponsor_id:
                raise BusinessValidationError(
                    status_code=403, 
                    error_message="Campaign does not belong to the sponsor."
                )
        
        ad_requests = []
        for ad_request in campaign.ad_requests:
            influencer = ad_request.influencer
            ad = {
                'id': ad_request.id,
                'requirement': ad_request.requirement,
                'payment_amount': ad_request.payment_amount,
                'message': ad_request.message,
                'status': ad_request.status.name,
                'sender_user_id': ad_request.sender_user_id,
                'influencer': {
                    'id': influencer.id if influencer else None,
                    'name': influencer.name if influencer else None
                }
            }
            ad_requests.append(ad)
        
        goals = []
        for goal in campaign.goals:
            g = {
                'id': goal.id,
                'name': goal.name,
                'status': goal.status,
                'n_ads': len(goal.ad_requests)
            }
            goals.append(g)
        
        output = {
            'id': campaign.id,
            'name': campaign.name,
            'start_date': campaign.start_date,
            'end_date': campaign.end_date,
            'description': campaign.description,
            'budget': campaign.budget,
            'niche': {
                'id': campaign.niche.id,
                'name': campaign.niche.name
            },
            'visibility': {
                'id': campaign.campaign_visibility.id,
                'name': campaign.campaign_visibility.name
            },
            'ad_requests': ad_requests,
            'goals': goals,
            'flagged': campaign.flagged
        }

        return output

    @auth_required('token')
    @roles_required('Sponsor')
    def put(self, campaign_id):
        campaign_args = campaign_parser.parse_args()
        name = campaign_args.get("name")
        description = campaign_args.get("description")
        budget = campaign_args.get("budget")
        visibility_id = campaign_args.get("visibility_id")
        niche_id = campaign_args.get("niche_id")
        start_date = campaign_args.get("start_date")
        end_date = campaign_args.get("end_date")

        if not budget:
            budget = 0

        if budget < 0:
            raise BusinessValidationError(
                status_code=403,
                error_message="Campaign budget cannot be less than 0."
            )

        if not (name and start_date and end_date and visibility_id and niche_id):
            raise IncompleteDataProvidedError()

        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # sponsor = db.session.get(Sponsor, sponsor_id)
        sponsor = current_user.sponsor
        if not sponsor:
            raise NotFoundError(error_message="Sponsor not found.")

        campaign = db.session.get(Campaign, campaign_id)
        if campaign.sponsor_id != sponsor.id:
            raise BusinessValidationError(
                status_code=403, 
                error_message="Campaign does not belong to the sponsor."
            )
        
        if start_date > end_date:
            raise BusinessValidationError(
                status_code=403, 
                error_message="End date cannot be before start date."
            )
        
        total_budget = sponsor.budget + campaign.budget
        if budget > total_budget:
            raise BusinessValidationError(
                status_code=403, 
                error_message="Campaign budget cannot be greater than total budget."
            )

        total_budget -= budget
        sponsor.budget = total_budget

        campaign.name = name
        campaign.description = description
        campaign.start_date = start_date
        campaign.end_date = end_date
        campaign.niche_id = niche_id
        campaign.budget = budget
        campaign.visibility_id = visibility_id
        campaign.sponsor = sponsor

        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            logging.error(f"Database error: {error}")
            raise BusinessValidationError(
                status_code=500,
                error_message="Database error."
            )

        return { 'message': 'Campaign edited successfully.' }

    @auth_required('token')
    @roles_required('Sponsor')
    def delete(self, campaign_id):
        campaign = db.session.get(Campaign, campaign_id)
        sponsor = current_user.sponsor

        if not campaign:
            raise NotFoundError(error_message="Campaign not found.")
        
        if campaign.sponsor_id != sponsor.id:
            raise BusinessValidationError(
                status_code=403, 
                error_message="Campaign does not belong to the sponsor."
            )
        
        sponsor = current_user.sponsor
        sponsor.budget += campaign.budget

        try:
            db.session.delete(campaign)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            logging.error(f"Database error: {error}")
            raise BusinessValidationError(
                status_code=500,
                error_message="Database error."
            )

        return { 'message': 'Campaign deleted successfully.' }

api.add_resource(CampaignAPI, "/campaign", "/campaign/<int:campaign_id>")

ad_request_fields = {
    'id': fields.Integer,
    'campaign_id': fields.Integer,
    'influencer_id': fields.Integer,
    'message': fields.String,
    'requirement': fields.String,
    'payment_amount': fields.Float,
    'status_id': fields.Integer,
    'sender_user_id': fields.Integer,
    'campaign_goal_id': fields.Integer,
}

ad_request_parser = reqparse.RequestParser()
ad_request_parser.add_argument("campaign_id", type=int)
ad_request_parser.add_argument("influencer_id")
ad_request_parser.add_argument("message", type=str)
ad_request_parser.add_argument("requirement", type=str)
ad_request_parser.add_argument("payment_amount", type=float)
ad_request_parser.add_argument("status_id")
ad_request_parser.add_argument("sender_user_id", type=int)
ad_request_parser.add_argument("campaign_goal_id", type=int)

class AdRequestAPI(Resource):
    @auth_required('token')
    @roles_accepted('Sponsor')
    @not_flagged()
    @not_approved()
    def post(self):
        ad_request_args = ad_request_parser.parse_args()
        campaign_id = ad_request_args.get('campaign_id')
        influencer_id = ad_request_args.get('influencer_id', None)
        message = ad_request_args.get('message')
        requirement = ad_request_args.get('requirement')
        payment_amount = ad_request_args.get('payment_amount')
        status_id = ad_request_args.get('status_id', 1)
        sender_user_id = ad_request_args.get('sender_user_id')
        campaign_goal_id = ad_request_args.get('campaign_goal_id')

        campaign = db.session.get(Campaign, campaign_id)

        if payment_amount > campaign.budget:
            raise BusinessValidationError(
                status_code=403, 
                error_message="Payment amount cannot be greater than total budget."
            )

        campaign.budget -= payment_amount

        ad_request = AdRequest(
            campaign_id=campaign_id,
            influencer_id=influencer_id,
            message=message,
            requirement=requirement,
            payment_amount=payment_amount,
            status_id=status_id,
            sender_user_id=sender_user_id,
            campaign_goal_id=campaign_goal_id
        )

        db.session.add(ad_request)
        db.session.commit()

        return { 'message': 'Ad Request created successfully.', 'id': ad_request.id }


    @auth_required('token')
    @roles_accepted('Sponsor', 'Influencer', 'Admin')
    @marshal_with(ad_request_fields)
    def get(self, ad_request_id):
        ad_request = db.session.get(AdRequest, ad_request_id)

        if not ad_request:
            raise NotFoundError(error_message="Ad request not found.")
        
        output = {
            'id': ad_request.id,
            'campaign_id': ad_request.campaign_id,
            'influencer_id': ad_request.influencer_id,
            'message': ad_request.message,
            'requirement': ad_request.requirement,
            'payment_amount': ad_request.payment_amount,
            'status_id': ad_request.status_id,
            'sender_user_id': ad_request.sender_user_id,
            'campaign_goal_id': ad_request.campaign_goal_id,
        }

        return output
    
    @auth_required('token')
    @roles_accepted('Sponsor', 'Influencer')
    def put(self, ad_request_id):
        ad_request_args = ad_request_parser.parse_args()
        campaign_id = ad_request_args.get('campaign_id')
        message = ad_request_args.get('message')
        requirement = ad_request_args.get('requirement')
        payment_amount = ad_request_args.get('payment_amount')
        campaign_goal_id = ad_request_args.get('campaign_goal_id')
        influencer_id = ad_request_args.get('influencer_id', None)

        campaign = db.session.get(Campaign, campaign_id)
        ad_request = db.session.get(AdRequest, ad_request_id)

        if not ad_request:
            raise NotFoundError(error_message="Ad request not found.")
        
        if ad_request.sender_user_id != current_user.id:
            raise BusinessValidationError(
                status_code=403, 
                error_message="You are not allowed to edit this ad request."
            )
        
        if ad_request.status.name != 'Pending':
            raise BusinessValidationError(
                status_code=403, 
                error_message="You can only edit a 'Pending' ad request."
            )

        total_budget = campaign.budget + ad_request.payment_amount

        if payment_amount > total_budget:
            raise BusinessValidationError(
                status_code=403, 
                error_message="Payment amount cannot be greater than total budget."
            )

        campaign.budget = total_budget - payment_amount
        
        ad_request.message = message
        ad_request.requirement = requirement
        ad_request.payment_amount = payment_amount
        ad_request.influencer_id = influencer_id
        ad_request.campaign_goal_id = campaign_goal_id
        ad_request.sender_user_id = current_user.id
        ad_request.status_id = 1

        db.session.commit()

        return { 'message': 'Ad Request created successfully.', 'id': ad_request.id, 'campaign_id': ad_request.campaign.id }

    @auth_required('token')
    @roles_accepted('Sponsor', 'Influencer')
    def delete(self, ad_request_id):
        ad_request = db.session.get(AdRequest, ad_request_id)

        if not ad_request:
            raise BusinessValidationError(
                status_code=404, 
                error_message="Ad request not found."
            )

        if ad_request.sender_user_id != current_user.id:
            raise BusinessValidationError(
                status_code=403, 
                error_message="You cannot delete this ad request."
            )

        ad_request.campaign.budget += ad_request.payment_amount

        db.session.delete(ad_request)
        db.session.commit()

        return { 'message': 'Ad Request deleted successfully.' }

api.add_resource(AdRequestAPI, '/ad-request', '/ad-request/<int:ad_request_id>')

influencer_serach_parser = reqparse.RequestParser()
influencer_serach_parser.add_argument("min_reach")
influencer_serach_parser.add_argument("category_id")
influencer_serach_parser.add_argument("niche", type=str)

class InfluencerSearchAPI(Resource):
    @auth_required('token')
    @roles_accepted('Sponsor')
    def post(self):
        influencer_serach_args = influencer_serach_parser.parse_args()
        min_reach = influencer_serach_args.get("min_reach", None)
        category_id = influencer_serach_args.get("category_id", None)
        niche = influencer_serach_args.get("niche", None)

        unflagged_user_ids = [user.id for user in db.session.query(User).filter(User.flagged == False).all()]

        query = db.session.query(Influencer)

        if min_reach:
            query = query.filter(Influencer.reach >= min_reach)
        
        if category_id:
            query = query.filter(Influencer.category_id == category_id)

        if niche:
            query = query.filter((Influencer.niche.like(f"%{niche}%")) | (Influencer.name.like(f"%{niche}%")))

        filtered_influencers = [influencer for influencer in query.all() if influencer.user_id in unflagged_user_ids]

        influencers = []
        for influencer in filtered_influencers:
            influ = {
                'id': influencer.id,
                'name': influencer.name,
                'category': influencer.category.name,
                'niche': influencer.niche,
                'reach': influencer.reach,
                'user_id': influencer.user_id,
            }
            influencers.append(influ)

        return { 'data': influencers }

api.add_resource(InfluencerSearchAPI, '/search/influencers')

campaign_search_parser = reqparse.RequestParser()
campaign_search_parser.add_argument("min_budget")
campaign_search_parser.add_argument("niche_id")
campaign_search_parser.add_argument("keyword", type=str)


class CampaignSearchAPI(Resource):
    @auth_required('token')
    @roles_accepted('Influencer')
    # @marshal_with(campaign_fields)
    def post(self):
        campaign_search_args = campaign_search_parser.parse_args()
        min_budget = campaign_search_args.get("min_budget", None)
        niche_id = campaign_search_args.get("niche_id", None)
        keyword = campaign_search_args.get("keyword", None)

        query = db.session.query(Campaign).filter((Campaign.flagged == False) & (Campaign.visibility_id == 1) & (Campaign.end_date > datetime.today().date()))

        if min_budget:
            query = query.filter(Campaign.budget >= min_budget)
        
        if niche_id:
            query = query.filter(Campaign.niche_id == niche_id)

        if keyword:
            query = query.filter((Campaign.name.like(f"%{keyword}%")) | (Campaign.description.like(f"%{keyword}%")))

        filtered_campaigns = query.all()
        campaigns = []
        for campaign in filtered_campaigns:
            camp = {
                'id': campaign.id,
                'name': campaign.name,
                'description': campaign.description,
                'start_date': str(campaign.start_date),
                'end_date': str(campaign.end_date),
                'budget': campaign.budget,
                'visibility': campaign.campaign_visibility.name,
                'niche': campaign.niche.name,
                'sponsor': campaign.sponsor.name,
                'flagged': campaign.flagged,
            }
            campaigns.append(camp)
        
        return { 'data': campaigns }

api.add_resource(CampaignSearchAPI, '/search/campaigns')
