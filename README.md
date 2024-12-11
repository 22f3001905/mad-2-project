## Influencer Engagement & Sponsorship Co-ordination Platform - V2

### API Authentication

* URL: POST on `http://localhost:8080/login?include_auth_token` with credentials in body.
* URL: GET on `http://localhost:8080/admin` will require the Authentication-Token Header and Role as 'Admin'.

### Commands

1. Vue: npm run dev
2. Server: python server.py
3. Redis: redis-server --port 6375
4. Celery Worker: celery -A celery_service.celery_app worker --loglevel INFO
5. Mailhog: MailHog
6. Celery Beat: celery -A celery_service.celery_app beat --max-interval 30 --loglevel INFO

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
