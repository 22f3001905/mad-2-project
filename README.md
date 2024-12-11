## Influencer Engagement & Sponsorship Co-ordination Platform - V2

### API Authentication

* URL: POST on `http://localhost:8080/login?include_auth_token` with credentials in body.
* URL: GET on `http://localhost:8080/admin` will require the Authentication-Token Header and Role as 'Admin'.

### Commands

```bash
# Vue
npm run dev

# Flask
python server.py

# Redis
redis-server --port 6375

# MailHog
MailHog

# Celery
celery -A celery_service.celery_app worker --loglevel INFO
celery -A celery_service.celery_app beat --max-interval 30 --loglevel INFO
```

### Installation

```bash
npm install
npm run dev

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py

python dummy_data.py
```
