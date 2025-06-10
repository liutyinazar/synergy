import asyncio
from typing import Dict

import httpx
from celery import Task
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.celery_app import celery_app
from app.core.config import get_settings
from app.models.credit_card import CreditCard

settings = get_settings()


@celery_app.task(bind=True)
def fetch_credit_cards(self: Task) -> Dict[str, str]:
    async def _fetch_credit_cards() -> Dict[str, str]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.API_BASE_URL}/creditCards?_quantity=5"
            )
            if response.status_code == 200:
                credit_cards_data = response.json()["data"]

                # Connect to MongoDB
                mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
                db = mongo_client[str(settings.DATABASE_NAME)]
                collection = db.credit_cards

                # Get random user IDs
                users_collection = db.users
                users = await users_collection.find().to_list(length=5)

                # Insert credit cards with user IDs
                for card_data, user in zip(credit_cards_data, users):
                    credit_card = CreditCard(
                        type=card_data["type"],
                        number=card_data["number"],
                        expiration=card_data["expiration"],
                        owner=card_data["owner"],
                        user_id=user["id"],
                    )
                    await collection.update_one(
                        {"number": card_data["number"]},
                        {"$set": credit_card.dict()},
                        upsert=True,
                    )

                return {
                    "status": "success",
                    "message": f"Fetched {len(credit_cards_data)} credit cards",
                }
            return {
                "status": "error",
                "message": "Failed to fetch credit cards",
            }

    return asyncio.run(_fetch_credit_cards())
