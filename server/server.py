from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore

from app.config import LocalDevConfig
from app.models import db, User, Role
from app.resources import api
from app.utils import create_user
from app.mail import mail
from app.worker import celery_init_app
from app.cache import cache

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevConfig)

    CORS(app, origins=["http://localhost:8000"])

    db.init_app(app)
    api.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)

    app.app_context().push()
    return app

app = create_app()
celery_app = celery_init_app(app)

# Only run once.
with app.app_context():
    db.create_all()
    app.security.datastore.find_or_create_role(name="Admin", description="This is superuser.")
    app.security.datastore.find_or_create_role(name="Sponsor", description="This is sponsor.")
    app.security.datastore.find_or_create_role(name="Influencer", description="This is influencer.")

    db.session.commit()

    create_user(email="admin@website.com", password="admin", roles=["Admin", "Sponsor", "Influencer"])
    db.session.commit()

from app.routes import *

if __name__ == "__main__":
    app.run(port=5000)
