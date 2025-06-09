import httpx
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings
from app.core.celery_app import celery_app

settings = get_settings()


@celery_app.task
def fetch_addresses():
    async def _fetch_addresses():
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.API_BASE_URL}/addresses?_quantity=5"
            )
            if response.status_code == 200:
                addresses = response.json()["data"]

                # Connect to MongoDB
                client = AsyncIOMotorClient(settings.MONGODB_URL)
                db = client[settings.DATABASE_NAME]
                collection = db.addresses

                # Get random user IDs
                users_collection = db.users
                users = await users_collection.find().to_list(length=5)

                # Insert addresses with user IDs
                for address, user in zip(addresses, users):
                    address["user_id"] = user["id"]
                    await collection.update_one(
                        {"id": address["id"]}, {"$set": address}, upsert=True
                    )

                return {
                    "status": "success",
                    "message": f"Fetched {len(addresses)} addresses",
                }
            return {"status": "error", "message": "Failed to fetch addresses"}

    import asyncio

    return asyncio.run(_fetch_addresses())
