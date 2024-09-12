from flask import current_app as app
from flask_security import hash_password

def create_user(email, password, roles: list):
    user_exists = app.security.datastore.find_user(email=email)
    if not user_exists:
        hashed_password = hash_password(password)
        app.security.datastore.create_user(email=email, password=hashed_password, roles=roles)
