from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings
from app.models.user import User
from app.models.address import Address
from app.models.credit_card import CreditCard

app = FastAPI(title="User Data API")
settings = get_settings()

# MongoDB connection
client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]


@app.get("/users/", response_model=list[User])
async def get_users():
    users = await db.users.find().to_list(length=100)
    return users


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/{user_id}/address", response_model=Address)
async def get_user_address(user_id: int):
    address = await db.addresses.find_one({"user_id": user_id})
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@app.get("/users/{user_id}/credit-card", response_model=CreditCard)
async def get_user_credit_card(user_id: int):
    credit_card = await db.credit_cards.find_one({"user_id": user_id})
    if not credit_card:
        raise HTTPException(status_code=404, detail="Credit card not found")
    return credit_card
