from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.user", "app.tasks.address", "app.tasks.credit_card"],
)

celery_app.conf.beat_schedule = {
    "fetch-users": {
        "task": "app.tasks.user.fetch_users",
        "schedule": 60.0,  # every 1 minute
    },
    "fetch-addresses": {
        "task": "app.tasks.address.fetch_addresses",
        "schedule": 120.0,  # every 2 minutes
    },
    "fetch-credit-cards": {
        "task": "app.tasks.credit_card.fetch_credit_cards",
        "schedule": 180.0,  # every 3 minutes
    },
}
