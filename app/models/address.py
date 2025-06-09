from datetime import datetime
from pydantic import BaseModel, Field


class Address(BaseModel):
    id: int
    street: str
    streetName: str
    buildingNumber: str
    city: str
    zipcode: str
    country: str
    country_code: str
    latitude: float
    longitude: float
    user_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
