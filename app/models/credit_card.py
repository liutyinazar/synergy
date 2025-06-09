from datetime import datetime
from pydantic import BaseModel, Field


class CreditCard(BaseModel):
    type: str
    number: str
    expiration: str
    owner: str
    user_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
