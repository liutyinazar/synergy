import asyncio
from typing import Dict

import httpx
from celery import Task
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.celery_app import celery_app
from app.core.config import get_settings
from app.models.address import Address

settings = get_settings()


@celery_app.task(bind=True)
def fetch_addresses(self: Task) -> Dict[str, str]:
    async def _fetch_addresses() -> Dict[str, str]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.API_BASE_URL}/addresses?_quantity=5"
            )
            if response.status_code == 200:
                addresses_data = response.json()["data"]

                # Connect to MongoDB
                mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
                db = mongo_client[str(settings.DATABASE_NAME)]
                collection = db.addresses

                # Get random user IDs
                users_collection = db.users
                users = await users_collection.find().to_list(length=5)

                # Insert addresses with user IDs
                for address_data, user in zip(addresses_data, users):
                    address = Address(
                        **address_data,
                        user_id=user["id"],
                    )
                    await collection.update_one(
                        {"id": address_data["id"]},
                        {"$set": address.dict()},
                        upsert=True,
                    )

                return {
                    "status": "success",
                    "message": f"Fetched {len(addresses_data)} addresses",
                }
            return {
                "status": "error",
                "message": "Failed to fetch addresses",
            }

    return asyncio.run(_fetch_addresses())
