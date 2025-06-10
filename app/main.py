import logging
from typing import List

from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import get_settings
from app.models.address import Address
from app.models.credit_card import CreditCard
from app.models.user import User

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/app/logs/app.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

app = FastAPI()
settings = get_settings()


@app.get("/users", response_model=List[User])
async def get_users() -> List[User]:
    logger.info("Getting all users")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[str(settings.DATABASE_NAME)]
    users = await db.users.find().to_list(length=100)
    logger.info(f"Found {len(users)} users")
    return [User(**user) for user in users]


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int) -> User:
    logger.info(f"Getting user with id {user_id}")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[str(settings.DATABASE_NAME)]
    user = await db.users.find_one({"id": user_id})
    if user is None:
        logger.warning(f"User with id {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Found user with id {user_id}")
    return User(**user)


@app.get("/users/{user_id}/address", response_model=Address)
async def get_user_address(user_id: int) -> Address:
    logger.info(f"Getting address for user {user_id}")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[str(settings.DATABASE_NAME)]
    address = await db.addresses.find_one({"user_id": user_id})
    if address is None:
        logger.warning(f"Address for user {user_id} not found")
        raise HTTPException(status_code=404, detail="Address not found")
    logger.info(f"Found address for user {user_id}")
    return Address(**address)


@app.get("/users/{user_id}/credit-card", response_model=CreditCard)
async def get_user_credit_card(user_id: int) -> CreditCard:
    logger.info(f"Getting credit card for user {user_id}")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[str(settings.DATABASE_NAME)]
    credit_card = await db.credit_cards.find_one({"user_id": user_id})
    if credit_card is None:
        logger.warning(f"Credit card for user {user_id} not found")
        raise HTTPException(status_code=404, detail="Credit card not found")
    logger.info(f"Found credit card for user {user_id}")
    return CreditCard(**credit_card)
