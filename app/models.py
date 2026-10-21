from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class AdvertisementCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=2000)
    price: float = Field(..., gt=0)
    owner: str = Field(..., min_length=1, max_length=100)


class AdvertisementUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=2000)
    price: Optional[float] = Field(None, gt=0)
    owner: Optional[str] = Field(None, min_length=1, max_length=100)


class AdvertisementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    price: float
    owner: str
    created_at: datetime
