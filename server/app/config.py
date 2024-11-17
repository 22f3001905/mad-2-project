import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevConfig(Config):
    # SQL
    SQLALCHEMY_DATABASE_URI = "sqlite:///project.sqlite3"
    DEBUG = True

    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")

    WTF_CSRF_ENABLED = False  # Cross-Site Request Forgery
    SESSION_COOKIE_HTTPONLY = False
    SECURITY_TOKEN_AUTHENTICAION_HEADER = "Authentication-Token"  # Include in Request Header

    # SECURITY_CSRF_PROTECT = False
    # SESSION_COOKIE_NAME = None
    # SESSION_COOKIE_HTTPONLY = False

    # Mail
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = ('SponsorConnect', 'bot@sponsorconnect.com')

    # Caching
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 500  # Cache timeout in seconds
