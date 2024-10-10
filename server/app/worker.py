from celery import Celery, Task
from flask import Flask

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_config = dict(
        broker_url="redis://localhost:6375/0",
        result_backend="redis://localhost:6375/1",
        broker_connection_retry_on_startup = True,
        # result_expires = 3600
    )

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(celery_config)
    celery_app.set_default()
    app.extensions["celery"] = celery_app

    return celery_app
