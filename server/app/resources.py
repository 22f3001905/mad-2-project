from flask import current_app as app
from flask_restful import Api, Resource, reqparse
from flask_security import auth_required, roles_required

from app.utils import create_user
from app.models import db

api = Api()

user_parser = reqparse.RequestParser()
user_parser.add_argument("email")
user_parser.add_argument("password")
user_parser.add_argument("roles", type=str, action="append")  # roles: list

class UserAPI(Resource):
    def post(self):
        user_args = user_parser.parse_args()
        email = user_args.get("email")
        password = user_args.get("password")
        roles = user_args.get("roles")

        with app.app_context():
            create_user(email=email, password=password, roles=roles)
            db.session.commit()
            return {
                "message": "Successfully created user."
            }, 201
    
api.add_resource(UserAPI, "/user/create")
