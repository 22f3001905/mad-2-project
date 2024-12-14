## Influencer Engagement & Sponsorship Co-ordination Platform - V2

### API Authentication

* URL: POST on `http://localhost:8080/login?include_auth_token` with credentials in body.
* URL: GET on `http://localhost:8080/admin` will require the Authentication-Token Header and Role as 'Admin'.

### Installation Commands

```bash
# Vue.js
npm install
npm run dev

# Flask
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py

python dummy_data.py
```

### Additional Commands

```bash
# Redis
redis-server --port 6375

# MailHog (Port: 8025)
MailHog

# Celery
celery -A celery_service.celery_app worker --loglevel INFO
celery -A celery_service.celery_app beat --max-interval 30 --loglevel INFO
```
