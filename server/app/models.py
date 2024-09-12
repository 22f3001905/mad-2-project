from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

# Models: flask security rules (assumptions)
# Tables: User, Role
# Many-to-Many relationship between User and Role

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    roles = db.Relationship("Role", backref="bearers", secondary="users_roles")

    sponsor = db.relationship("Sponsor", uselist=False, backref="user", cascade="all, delete")
    influencer = db.relationship("Influencer", uselist=False, backref="user", cascade="all, delete")
    sent_ad_requests = db.relationship("AdRequest", backref="user", cascade="all, delete-orphan")

# ('Admin', 'Sponsor', 'Influencer')
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)

class UsersRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))

class Industry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    sponsors = db.relationship("Sponsor", backref="industry")

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    industry_id = db.Column(db.Integer, db.ForeignKey("industry.id"), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False, unique=True)
    campaigns = db.relationship("Campaign", backref="sponsor")

class InfluencerCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    influencers = db.relationship("Influencer", backref="category")

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("influencer_category.id"), nullable=False)
    niche = db.Column(db.String(255))
    reach = db.Column(db.Integer, nullable=False)  # No. of followers
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False, unique=True)
    assigned_ads = db.relationship("AdRequest", backref="influencer")
    wallet_balance = db.Column(db.Float, nullable=False, default=0)

# ('Public', 'Private')
class CampaignVisibility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    campaigns = db.relationship("Campaign", backref="campaign_visibility")

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    visibility_id = db.Column(db.Integer, db.ForeignKey("campaign_visibility.id"), nullable=False)
    niche_id = db.Column(db.Integer, db.ForeignKey("campaign_niche.id"), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey("sponsor.id"), nullable=False)
    ad_requests = db.relationship("AdRequest", backref="campaign", cascade="all, delete-orphan")
    goals = db.relationship("CampaignGoal", backref="campaign", cascade="all, delete-orphan")
    flagged = db.Column(db.Boolean, default=False)

class CampaignNiche(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    campaigns = db.relationship("Campaign", backref="niche")

class CampaignGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    # status = db.Column(db.String(80))  # ("Incomplete", "Completed")
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id", ondelete="CASCADE"), nullable=False)
    ad_requests = db.relationship("AdRequest", backref="campaign_goal")

# ('Pending', 'Accepted', 'Rejected', 'Completed')
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    ad_requests = db.relationship("AdRequest", backref="status")

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id", ondelete="CASCADE"), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey("influencer.id"), nullable=True)
    message = db.Column(db.String(255))
    requirement = db.Column(db.String(255), nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"), nullable=False)
    sender_user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    campaign_goal_id = db.Column(db.Integer, db.ForeignKey("campaign_goal.id"), nullable=False)
