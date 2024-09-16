import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///project.sqlite3"
    DEBUG = True

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")

    WTF_CSRF_ENABLED = False  # Cross-Site Request Forgery
    # SECURITY_CSRF_PROTECT = False
    SECURITY_TOKEN_AUTHENTICAION_HEADER = "Authentication-Token"  # Include in Request Header

    # SESSION_COOKIE_NAME = None
    # SESSION_COOKIE_HTTPONLY = False
