from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class OrderCreate(BaseModel):
    item: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    customer_id: str

class OrderUpdate(BaseModel):
    item: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[str] = Field(None, pattern=r"^(pending|completed|cancelled)$") 

class OrderInDB(OrderCreate):
    _id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
