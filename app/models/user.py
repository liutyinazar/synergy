from datetime import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    uuid: str
    firstname: str
    lastname: str
    username: str
    email: str
    ip: str
    macAddress: str
    website: str
    image: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
