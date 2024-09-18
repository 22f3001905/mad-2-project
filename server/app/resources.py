from flask import current_app as app
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_security import auth_required, roles_required, current_user, roles_accepted

from app.utils import create_user
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

        if roles[0] == "Sponsor":
            company_name = user_args.get("companyName")
            industry_id = user_args.get("industryId")
            sponsor = Sponsor(
                name=company_name,
                industry_id=industry_id,
                user=user
            )
            db.session.add(sponsor)
        else:
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

campaign_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "start_date": fields.DateTime(dt_format="iso8601"),
    "end_date": fields.DateTime(dt_format="iso8601"),
    "budget": fields.Float,
    "niche": fields.String,
    "visibility": fields.String,
    # "niche_id": fields.Integer,
    # "visibility_id": fields.Integer,
    # "sponsor_id": fields.Integer
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
    @marshal_with(campaign_fields)
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
        
        output = {
            'id': campaign.id,
            'name': campaign.name,
            'start_date': campaign.start_date,
            'end_date': campaign.end_date,
            'description': campaign.description,
            'budget': campaign.budget,
            'niche': campaign.niche.name,
            'visibility': campaign.campaign_visibility.name,
        }

        return output
    
    @auth_required('token')
    @roles_accepted('Sponsor', 'Influencer', 'Admin')
    @marshal_with(campaign_fields)
    def get(self, campaign_id):
        campaign = db.session.get(Campaign, campaign_id)
        
        if not campaign:
            raise NotFoundError(error_message="Campaign not found.")
        
        sponsor_id = current_user.sponsor.id
        
        if campaign.sponsor_id != sponsor_id:
            raise BusinessValidationError(
                status_code=403, 
                error_message="Campaign does not belong to the sponsor."
            )
        
        output = {
            'id': campaign.id,
            'name': campaign.name,
            'start_date': campaign.start_date,
            'end_date': campaign.end_date,
            'description': campaign.description,
            'budget': campaign.budget,
            'niche': campaign.niche.name,
            'visibility': campaign.campaign_visibility.name,
        }

        return output

    @auth_required('token')
    @roles_required('Sponsor')
    @marshal_with(campaign_fields)
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
        
        output = {
            'id': campaign.id,
            'name': campaign.name,
            'start_date': campaign.start_date,
            'end_date': campaign.end_date,
            'description': campaign.description,
            'budget': campaign.budget,
            'niche': campaign.niche.name,
            'visibility': campaign.campaign_visibility.name,
        }
        
        return output

    @auth_required('token')
    @roles_required('Sponsor')
    def delete(self, campaign_id):
        campaign = db.session.get(Campaign, campaign_id)

        if not campaign:
            raise NotFoundError(error_message="Campaign not found.")

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

        return None

api.add_resource(CampaignAPI, "/campaign", "/campaign/<int:campaign_id>")
