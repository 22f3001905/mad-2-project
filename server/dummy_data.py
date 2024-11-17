from server import app
app.app_context().push()

from app.models import *
from app.utils import create_user

from datetime import datetime
from flask_security import hash_password

def basic_setup():
    visi_names = ("Public", "Private")
    visis = []

    for visi_name in visi_names:
        visis.append(CampaignVisibility(name=visi_name))

    status_names = ('Pending', 'Accepted', 'Rejected', 'Completed')
    stati = []

    for status_name in status_names:
        stati.append(Status(name=status_name))

    industry_names = ('Fashion/Apparel', 'Food & Beverage', 'Beauty/Cosmetics', 'Travel', 'Health/Fitness', 'Technology', 'Entertainment', 'Automotive', 'Education', 'Other')
    industries = []

    for industry_name in industry_names:
        industries.append(Industry(name=industry_name))
    
    influencer_category_names = ('Fashion', 'Fitness', 'Travel', 'Food', 'Tech', 'Lifestyle', 'Education', 'Gaming', 'Finance', 'Other')
    influencer_categories = []

    for influencer_category_name in influencer_category_names:
        influencer_categories.append(InfluencerCategory(name=influencer_category_name))
    
    campaign_niche_names = ('Social Media Advertising', 'Video Advertising', 'Sponsored Content', 'Affiliate Marketing', 'Sponsored Posts', 'Other')
    campaign_niches = []

    for niche_name in campaign_niche_names:
        campaign_niches.append(CampaignNiche(name=niche_name))
    
    
    db.session.add_all(visis)
    db.session.add_all(stati)
    db.session.add_all(industries)
    db.session.add_all(influencer_categories)
    db.session.add_all(campaign_niches)
    db.session.commit()

def create_dummy_sponsor(email, password, company_name, industry_id, budget, flagged=False):
    user = create_user(email, password, ["Sponsor"])

    if user == None:
        return { "message": "User cannot be created." }

    sponsor = Sponsor(
        name=company_name,
        industry_id=industry_id,
        budget=budget,
        user=user
    )
    db.session.add(sponsor)

def create_dummy_influencer(email, password, influencer_name, category_id, niche, reach, flagged=False):
    user = create_user(email, password, ["Influencer"])

    if user == None:
        return { "message": "User cannot be created." }
    
    influencer = Influencer(
        name=influencer_name,
        category_id=category_id,
        niche=niche,
        reach=reach,
        user=user
    )
    db.session.add(influencer)

def create_dummy_campaign(name, description, start_date, end_date, niche_id, budget, goals, sponsor_id, visibility_id=1):
    campaign = Campaign(
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        niche_id=niche_id,
        budget=budget,
        visibility_id=visibility_id,
        sponsor_id=sponsor_id
    )

    db.session.add(campaign)

    goals: list = [goal.strip() for goal in goals.split("\n")]
    for goal in goals:
        campaign_goal = CampaignGoal(
            name=goal,
            # status="Incomplete",
            campaign=campaign
        )
        db.session.add(campaign_goal)
    
    # db.session.commit()

def create_dummy_ad_request(campaign_id, influencer_id, requirement, message, payment_amount, sender_user_id, campaign_goal_id, status_id=1):
    ad_request = AdRequest(
        campaign_id=campaign_id, 
        influencer_id=influencer_id, 
        requirement=requirement, 
        message=message, 
        payment_amount=payment_amount, 
        sender_user_id=sender_user_id, 
        campaign_goal_id=campaign_goal_id, 
        status_id=status_id
    )

    db.session.add(ad_request)
    # db.session.commit()


def input_data():
    dummy_sponsors: list = [
        {
            "email": "contact@myntra.com",
            "password": "fashion",
            "company_name": "Myntra Fashion",
            "industry_id":1, 
            "budget":150_000
        },
        {
            "email": "contact@nordvpn.com", 
            "password": "nordic", 
            "company_name": "Nord VPN", 
            "industry_id": 10, 
            "budget": 150_000
        },
        {
            "email": "contact@apple.com", 
            "password": "apple", 
            "company_name": "Apple Inc.", 
            "industry_id": 6, 
            "budget": 250_000
        },
        {
            "email": "contact@amazon.com", 
            "password": "prime", 
            "company_name": "Amazon Prime", 
            "industry_id": 7, 
            "budget": 250_000
        }
    ]

    for sponsor in dummy_sponsors:
        create_dummy_sponsor(**sponsor)
    
    db.session.commit()
    
    dummy_influencers: list = [
        {
            "email": "healthy.gamer@website.com",
            "password": "gamer",
            "influencer_name": "Healthy Gamer",
            "category_id": 7,
            "niche": "mental health, psychology, educational, wellness, editation, therapy",
            "reach": 500_000
        },
        {
            "email": "kurt.vlogs@website.com",
            "password": "travel",
            "influencer_name": "Kurt Caz Vlogs",
            "category_id": 3,
            "niche": "travel, culture, food, cusines, altruism, vlogs, heritage sites",
            "reach": 350_000
        },
        {
            "email": "lex@website.com",
            "password": "ai",
            "influencer_name": "Lex Podcast",
            "category_id": 7,
            "niche": "machine learning, ai, artificial intelligence, podcast, scientists, physics, psychology, robots",
            "reach": 300_000
        },
        {
            "email": "fit.emma@website.com",
            "password": "fitness",
            "influencer_name": "Emma Fitness",
            "category_id": 2,
            "niche": "fitness, workout routines, nutrition, wellness, bodybuilding, healthy living",
            "reach": 600_000
        },
        {
            "email": "tech.guru@website.com",
            "password": "gadgets",
            "influencer_name": "Tech Guru",
            "category_id": 5,
            "niche": "technology, reviews, gadgets, smartphones, computers, tech tutorials",
            "reach": 200_000
        },
        {
            "email": "anna.styles@website.com",
            "password": "vogue",
            "influencer_name": "Anna Styles",
            "category_id": 1,
            "niche": "fashion, styling tips, beauty, makeup tutorials, luxury brands, trends",
            "reach": 400_000
        },
        {
            "email": "foodie.hana@website.com",
            "password": "gourmet",
            "influencer_name": "Foodie Hana",
            "category_id": 4,
            "niche": "food, cooking, recipes, restaurant reviews, gourmet cuisine, street food",
            "reach": 280_000
        },
        {
            "email": "coder.ada@website.com",
            "password": "coding",
            "influencer_name": "Coder Ada",
            "category_id": 5,
            "niche": "programming, coding tutorials, software development, tech trends, AI, machine learning",
            "reach": 630_000
        },
        {
            "email": "live.learner@website.com",
            "password": "knowledge",
            "influencer_name": "Live Learner",
            "category_id": 7,
            "niche": "educational, science, history, tutorials, study tips, academic advice, productivity, experiments",
            "reach": 200_000,
            "flagged": True
        },
        {
            "email": "pixel.zoey@website.com",
            "password": "pixel",
            "influencer_name": "Pixel Zoey",
            "category_id": 8,
            "niche": "gaming, RPGs, game reviews, cosplay, live streaming, fantasy games",
            "reach": 420_000
        },
        {
            "email": "gaming.god@website.com",
            "password": "esports",
            "influencer_name": "Gaming God Gopal",
            "category_id": 8,
            "niche": "gaming, esports, game reviews, live streams, gaming tutorials, tech",
            "reach": 700_000
        },
        {
            "email": "finance.master@website.com",
            "password": "wealth",
            "influencer_name": "Finance Master Mohit",
            "category_id": 9,
            "niche": "finance, investing, personal finance, stock market, savings tips, economic trends",
            "reach": 520_000
        },
        {
            "email": "alice.art@website.com",
            "password": "creativity",
            "influencer_name": "Art with Alice",
            "category_id": 10,
            "niche": "art, painting, drawing tutorials, art history, creative projects, DIY crafts",
            "reach": 270_000
        }
    ]

    for influencer in dummy_influencers:
        create_dummy_influencer(**influencer)
    
    db.session.commit()
    
    myntra_campaigns = [
        {
            "name": "End of Reason Sale",
            "description": "Showcase products that are at flat 50% discount.",
            "start_date": datetime.strptime("2024-05-12", "%Y-%m-%d").date(),
            "end_date": datetime.strptime("2025-02-12", "%Y-%m-%d").date(),
            "niche_id": 4,
            "budget": 50_000,
            "goals": "Reach brand recognition to 1.5M users\nIncrease sales by 20% from last year",
            "sponsor_id": 1
        },
        {
            "name": "Social Media Promotion",
            "description": "Promote selected brands on social media through influencers.",
            "start_date": datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
            "end_date": datetime.strptime("2025-01-01", "%Y-%m-%d").date(),
            "niche_id": 1,
            "budget": 50_000,
            "goals": "Increase click through rate that leads to purchase by 30%\nGain at least 5,000 new customers",
            "visibility_id": 2,
            "sponsor_id": 1
        },
        {
            "name": "Festival Bonanza",
            "description": "Highlight festive collection and special offers.",
            "start_date": datetime.strptime("2024-08-01", "%Y-%m-%d").date(),
            "end_date": datetime.strptime("2024-10-31", "%Y-%m-%d").date(),
            "niche_id": 5,
            "budget": 30_000,
            "goals": "Boost seasonal sales by 25%\nExpand customer base by 10K",
            "sponsor_id": 1
        },
        {
            "name": "Delete This Campaign",
            "description": "Promote selected brands on social media.",
            "start_date": datetime.strptime("2024-07-10", "%Y-%m-%d").date(),
            "end_date": datetime.strptime("2025-01-12", "%Y-%m-%d").date(),
            "niche_id": 1,
            "budget": 0,
            "goals": "Delete Success!",
            "sponsor_id": 1
        }
    ]

    def sponsor_adjust_budget(campaign):
        sponsor = db.session.get(Sponsor, campaign["sponsor_id"])
        sponsor.budget -= campaign["budget"]

    for campaign in myntra_campaigns:
        sponsor_adjust_budget(campaign)
        create_dummy_campaign(**campaign)
    
    db.session.commit()

    myntra_ad_requests = [
        {
            "campaign_id": 1,
            "influencer_id": 6,
            "requirement": "Ad of 30s in the intro for 5 videos.",
            "message": "Make sure to add additional info in the description.",
            "payment_amount": 10_000,
            "status_id": 1,
            "sender_user_id": 2,
            "campaign_goal_id": 1
        },
        {
            "campaign_id": 2,
            "influencer_id": 4,
            "requirement": "Unboxing and review in one video.",
            "message": "Highlight the unique features about the product.",
            "payment_amount": 10_000,
            "status_id": 2,
            "sender_user_id": 2,
            "campaign_goal_id": 3
        },
        {
            "campaign_id": 3,
            "influencer_id": None,
            "requirement": "Promote products in YouTube Shorts for 3 days.",
            "message": "Tag the official Myntra account.",
            "payment_amount": 5_000,
            "status_id": 1,
            "sender_user_id": 2,
            "campaign_goal_id": 5
        },
        {
            "campaign_id": 2,
            "influencer_id": 4,
            "requirement": "Create a dedicated product video.",
            "message": "Focus on the quality and design.",
            "payment_amount": 10_000,
            "status_id": 1,
            "sender_user_id": 2,
            "campaign_goal_id": 4
        },
        {
            "campaign_id": 3,
            "influencer_id": None,
            "requirement": "Live stream product launch for at least of 4 hours.",
            "message": "Engage with the audience and answer questions.",
            "payment_amount": 15_000,
            "status_id": 1,
            "sender_user_id": 2,
            "campaign_goal_id": 6
        }
    ]

    def campaign_adjust_budget(ad_request):
        campaign = db.session.get(Campaign, ad_request["campaign_id"])
        campaign.budget -= ad_request["payment_amount"]
    
    def influencer_payment(ad_request):
        if ad_request["status_id"] == 4:
            influencer = db.session.get(Influencer, ad_request["influencer_id"])
            influencer.wallet_balance += ad_request["payment_amount"]
    
    for ad_request in myntra_ad_requests:
        campaign_adjust_budget(ad_request)
        influencer_payment(ad_request)
        create_dummy_ad_request(**ad_request)
    
    db.session.commit()


    nord_campaigns = [
        {
            "name": "Nord VPN Sale",
            "description": "Using influencer specific coupon code, followers can get a discount.",
            "start_date": datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
            "end_date": datetime.strptime("2024-09-15", "%Y-%m-%d").date(),
            "niche_id": 2,
            "budget": 50_000,
            "goals": "Gain at least 5,000 new overseas users.\nIncrease sales revenue by 10%",
            "sponsor_id": 2
        },
        {
            "name": "VPN Services",
            "description": "Create YouTube tutorials on how and why to use our app.",
            "start_date": datetime.strptime("2024-07-01", "%Y-%m-%d").date(),
            "end_date": datetime.strptime("2024-11-01", "%Y-%m-%d").date(),
            "niche_id": 3,
            "budget": 50_000,
            "goals": "Increase free tier downloads by 20%\nCreate a presence in the VPN market.",
            "visibility_id": 2,
            "sponsor_id": 2
        }
    ]

    for campaign in nord_campaigns:
        sponsor_adjust_budget(campaign)
        create_dummy_campaign(**campaign)

    db.session.commit()

    nord_ad_requests = [
        {
            "campaign_id": 5,
            "influencer_id": None,
            "requirement": "Include a 60s promo ad in 5 live stream.",
            "message": "Mention the benefits of using NordVPN for gaming.",
            "payment_amount": 25_000,
            "status_id": 1,
            "sender_user_id": 3,
            "campaign_goal_id": 9
        },
        {
            "campaign_id": 6,
            "influencer_id": 8,
            "requirement": "Create a detailed review video about NordVPN.",
            "message": "Highlight the security features and ease of use.",
            "payment_amount": 20_000,
            "status_id": 1,
            "sender_user_id": 3,
            "campaign_goal_id": 11
        },
        {
            "campaign_id": 5,
            "influencer_id": None,
            "requirement": "Add a 30s ad spot in 10 videos.",
            "message": "Include a special promo code for your audience.",
            "payment_amount": 15_000,
            "status_id": 1,
            "sender_user_id": 3,
            "campaign_goal_id": 9
        },
        {
            "campaign_id": 6,
            "influencer_id": 5,
            "requirement": "Write a blog post about the importance of VPNs.",
            "message": "Explain how NordVPN protects user privacy.",
            "payment_amount": 10_000,
            "status_id": 4,
            "sender_user_id": 3,
            "campaign_goal_id": 10
        }
    ]

    for ad_request in nord_ad_requests:
        campaign_adjust_budget(ad_request)
        influencer_payment(ad_request)
        create_dummy_ad_request(**ad_request)

    db.session.commit()

    apple_campaigns = [
        {
            "name": "Apple Back to School",
            "description": "Offer students and educators discounts on MacBooks and iPads.",
            "start_date": datetime.strptime("2024-07-15", "%Y-%m-%d").date(),
            "end_date": datetime.strptime("2024-09-15", "%Y-%m-%d").date(),
            "niche_id": 4,
            "budget": 80_000,
            "goals": "Increase sales in the education sector by 15%\nBoost awareness of Apple's educational discounts.",
            "sponsor_id": 3
        },
        {
            "name": "iPhone Launch",
            "description": "Promote the latest iPhone.",
            "start_date": datetime.strptime("2024-09-01", "%Y-%m-%d").date(),
            "end_date": datetime.strptime("2024-10-31", "%Y-%m-%d").date(),
            "niche_id": 1,
            "budget": 100_000,
            "goals": "Drive pre-orders to exceed previous model by 20%\nIncrease social media engagement by 30%.",
            "sponsor_id": 3
        }
    ]

    for campaign in apple_campaigns:
        sponsor_adjust_budget(campaign)
        create_dummy_campaign(**campaign)

    db.session.commit()

    apple_ad_requests = [
        {
            "campaign_id": 7,
            "influencer_id": 3,
            "requirement": "Create a detailed tutorial for using Apple products for school.",
            "message": "Show how Apple products enhance productivity.",
            "payment_amount": 20_000,
            "status_id": 4,
            "sender_user_id": 8,
            "campaign_goal_id": 13
        },
        {
            "campaign_id": 8,
            "influencer_id": None,
            "requirement": "Review the latest iPhone in your tech channel.",
            "message": "Highlight the new features and improvements.",
            "payment_amount": 25_000,
            "status_id": 1,
            "sender_user_id": 4,
            "campaign_goal_id": 14
        },
        {
            "campaign_id": 8,
            "influencer_id": None,
            "requirement": "Showcase the iPhone in a series of Instagram stories.",
            "message": "Tag the official Apple account and use the campaign hashtag.",
            "payment_amount": 10_000,
            "status_id": 1,
            "sender_user_id": 4,
            "campaign_goal_id": 15
        },
        {
            "campaign_id": 7,
            "influencer_id": 11,
            "requirement": "Feature Apple products in a back-to-school haul video.",
            "message": "Explain why these products are essential for students.",
            "payment_amount": 15_000,
            "status_id": 2,
            "sender_user_id": 4,
            "campaign_goal_id": 12
        },
        {
            "campaign_id": 8,
            "influencer_id": None,
            "requirement": "Create a comparison video between the new iPhone and its predecessor.",
            "message": "Focus on performance and camera quality.",
            "payment_amount": 10_000,
            "status_id": 1,
            "sender_user_id": 4,
            "campaign_goal_id": 14
        }
    ]

    for ad_request in apple_ad_requests:
        campaign_adjust_budget(ad_request)
        influencer_payment(ad_request)
        create_dummy_ad_request(**ad_request)

    db.session.commit()

    amazon_campaigns = [
        {
            "name": "Big Billion Day Sale",
            "description": "Offer exclusive deals to Prime members on a wide range of products.",
            "start_date": datetime.strptime("2024-07-15", "%Y-%m-%d").date(),
            "end_date": datetime.strptime("2025-02-16", "%Y-%m-%d").date(),
            "niche_id": 4,
            "budget": 75_000,
            "goals": "Increase Prime membership sign-ups by 25%\nBoost sales revenue during the event by 50%.",
            "sponsor_id": 4
        },
        {
            "name": "Prime Video Originals",
            "description": "Promote new original series and movies on Prime Video.",
            "start_date": datetime.strptime("2024-08-01", "%Y-%m-%d").date(),
            "end_date": datetime.strptime("2024-12-31", "%Y-%m-%d").date(),
            "niche_id": 1,
            "budget": 100_000,
            "goals": "Increase viewership of Prime Video by 20%\nGain at least 1 million new Prime Video subscribers.",
            "sponsor_id": 4
        }
    ]

    for campaign in amazon_campaigns:
        sponsor_adjust_budget(campaign)
        create_dummy_campaign(**campaign)

    db.session.commit()

    amazon_ad_requests = [
        {
            "campaign_id": 9,
            "influencer_id": 2,
            "requirement": "Create a haul video featuring products from the Big Billion Day Sale.",
            "message": "Highlight the discounts and deals.",
            "payment_amount": 30_000,
            "status_id": 1,
            "sender_user_id": 7,
            "campaign_goal_id": 17
        },
        {
            "campaign_id": 10,
            "influencer_id": None,
            "requirement": "Review and promote the latest Prime Video Originals series.",
            "message": "Provide your honest opinion and encourage subscriptions.",
            "payment_amount": 25_000,
            "status_id": 1,
            "sender_user_id": 5,
            "campaign_goal_id": 18
        },
        {
            "campaign_id": 9,
            "influencer_id": None,
            "requirement": "Create a shopping guide for the Big Billion Day Sale.",
            "message": "Focus on the best deals and offers.",
            "payment_amount": 20_000,
            "status_id": 1,
            "sender_user_id": 5,
            "campaign_goal_id": 16
        },
        {
            "campaign_id": 10,
            "influencer_id": 13,
            "requirement": "Make a video about your favorite Prime Video Originals series.",
            "message": "Discuss what makes the series unique and what you liked the most.",
            "payment_amount": 30_000,
            "status_id": 2,
            "sender_user_id": 5,
            "campaign_goal_id": 18
        },
        {
            "campaign_id": 10,
            "influencer_id": None,
            "requirement": "Ad of 30s in the intro for 5 videos.",
            "message": "Make sure to add additional info in the description.",
            "payment_amount": 10_000,
            "status_id": 1,
            "sender_user_id": 5,
            "campaign_goal_id": 19
        }
    ]

    for ad_request in amazon_ad_requests:
        campaign_adjust_budget(ad_request)
        influencer_payment(ad_request)
        create_dummy_ad_request(**ad_request)

    db.session.commit()

if __name__ == "__main__":
    basic_setup()
    input_data()
