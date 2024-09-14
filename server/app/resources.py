from flask import current_app as app
from flask_restful import Api, Resource, reqparse
from flask_security import auth_required, roles_required, hash_password

from app.utils import create_user
from app.models import db
from app.models import *

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
