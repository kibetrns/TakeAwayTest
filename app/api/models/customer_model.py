from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class CustomerCreate(BaseModel):
    full_name: str = Field(..., min_length=1)
    email_address: EmailStr
    phone_number: str = Field(..., pattern=r"^\+\d{1,3}\d{9,15}$")

class CustomerUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1)
    email_address: Optional[EmailStr]
    phone_number: Optional[str] = Field(None, pattern=r"^\+\d{1,3}\d{9,15}$")

class CustomerInDB(CustomerCreate):
    _id: str
    created_at: datetime