import asyncio
from typing import Dict

import httpx
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.celery_app import celery_app
from app.core.config import get_settings

settings = get_settings()


@celery_app.task
def fetch_users() -> Dict[str, str]:
    async def _fetch_users() -> Dict[str, str]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.API_BASE_URL}/users")
            if response.status_code == 200:
                users = response.json()["data"]

                # Connect to MongoDB
                mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
                db = mongo_client[str(settings.DATABASE_NAME)]
                collection = db.users

                # Insert users
                for user in users:
                    await collection.update_one(
                        {"id": user["id"]}, {"$set": user}, upsert=True
                    )

                return {
                    "status": "success",
                    "message": f"Fetched {len(users)} users",
                }
            return {"status": "error", "message": "Failed to fetch users"}

    return asyncio.run(_fetch_users())
