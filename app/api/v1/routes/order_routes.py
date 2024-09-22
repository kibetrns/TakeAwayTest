from fastapi import APIRouter
from app.api.models.order_model import OrderCreate, OrderInDB, OrderUpdate
from app.api.services.order_service import OrderService
from app.api.core.database import db

router = APIRouter()

@router.post("/orders/", response_model=OrderInDB)
async def create_order(order: OrderCreate):
    service = OrderService(db)
    return await service.create_order(order)

@router.get("/orders/{order_id}", response_model=OrderInDB)
async def get_order(order_id: str):
    service = OrderService(db)
    return await service.get_order(order_id)

@router.put("/orders/{order_id}", response_model=OrderInDB)
async def update_order(order_id: str, order_update: OrderUpdate):
    service = OrderService(db)
    return await service.update_order(order_id, order_update)

@router.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    service = OrderService(db)
    return await service.delete_order(order_id)
