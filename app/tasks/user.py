import httpx
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings
from app.core.celery_app import celery_app

settings = get_settings()


@celery_app.task
def fetch_users():
    async def _fetch_users():
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.API_BASE_URL}/users")
            if response.status_code == 200:
                users = response.json()["data"]

                # Connect to MongoDB
                client = AsyncIOMotorClient(settings.MONGODB_URL)
                db = client[settings.DATABASE_NAME]
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

    import asyncio

    return asyncio.run(_fetch_users())
