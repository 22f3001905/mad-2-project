### API Authentication

URL: POST on http://localhost:8080/login?include_auth_token with credentials in body.
URL: GET on http://localhost:8080/admin will require the Authentication-Token Header and Role as 'Admin'.

Commands to run:

1. Vue: npm run dev
2. Server: python server.py
3. Redis: redis-server --port 6375
4. Celery Worker: celery -A celery_service.celery_app worker --loglevel INFO
5. Celery Beat: celery -A celery_service.celery_app beat --max-interval 1 --loglevel INFO
