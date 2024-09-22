from fastapi import APIRouter
from app.api.models.customer_model import CustomerCreate, CustomerInDB, CustomerUpdate
from app.api.services.customer_service import CustomerService
from app.api.core.database import db

router = APIRouter()

@router.post("/customers/", response_model=CustomerCreate)
async def create_customer(customer: CustomerCreate):
    service = CustomerService(db)
    return await service.create_customer(customer.dict())

@router.get("/customers/{customer_id}", response_model=CustomerInDB)
async def get_customer(customer_id: str):
    service = CustomerService(db)
    return await service.get_customer(customer_id)

@router.put("/customers/{customer_id}", response_model=CustomerInDB)
async def update_customer(customer_id: str, customer_update: CustomerUpdate):
    service = CustomerService(db)
    return await service.update_customer(customer_id, customer_update)

@router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: str):
    service = CustomerService(db)
    return await service.delete_customer(customer_id)