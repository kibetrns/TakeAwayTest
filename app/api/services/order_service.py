import logging
from app.api.services.sms_alert_service import SMSAlertService
from bson.errors import InvalidId

from app.api.models.order_model import OrderInDB, OrderCreate, OrderUpdate
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from app.api.core.config import  settings
from app.api.services.customer_service import CustomerService

logger = logging.getLogger(__name__)

class OrderService:
    def __init__(self, db):
        self.db = db
        self.sms_service = SMSAlertService(settings.africastalking_username, settings.africastalking_api_key)
        self.customer_service = CustomerService(db)


    async def create_order(self, order_data: OrderCreate):
        order_data_dict = order_data.dict()
        order_data_dict['created_at'] = datetime.utcnow()
        order_data_dict['updated_at'] = datetime.utcnow()

        try:
            if not ObjectId.is_valid(order_data.customer_id):
                raise HTTPException(status_code=400, detail="Invalid customer ID. Must be a valid ObjectId.")
            order_data_dict['customer_id'] = ObjectId(order_data.customer_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Provide a valid ObjectId. The one you've provided is NOT valid.")

        try:
            logger.info(f"Creating new order with data: {order_data_dict}")
            result = await self.db.orders.insert_one(order_data_dict)
            order_id = result.inserted_id
            logger.info(f"Order created successfully with ID: {order_id}")

            customer = await self.customer_service.get_customer(order_data.customer_id)

            message = (
                f"Hello {customer.full_name}.\n \n"
                f"Your order of {order_data.item} with ID number {str(order_id)} has been placed successfully.\n \n "
                f"The total price is {order_data.price}. \n \n"
                f"Thank you for your order. We appreciate your business!"
            )

            self.sms_service.send_sms(customer.phone_numer, message)

            order_data_dict['_id'] = str(order_id)
            order_data_dict['customer_id'] = str(order_data_dict['customer_id'])  # Convert ObjectId to string

            return OrderInDB(**order_data_dict)
        except Exception as e:
            logger.error(f"Error occurred while creating order: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    async def get_order(self, order_id: str):
        try:
            obj_id = ObjectId(order_id)
            logger.info(f"Fetching order with ID: {order_id}")
        except Exception:
            logger.error(f"Invalid ObjectId provided: {order_id}")
            raise HTTPException(status_code=400, detail="Invalid ObjectId provided.")

        try:
            order = await self.db.orders.find_one({"_id": obj_id})
            if order is None:
                logger.warning(f"Order with ID {order_id} not found.")
                raise HTTPException(status_code=404, detail="Order NOT found.")
            order["_id"] = str(order["_id"])
            logger.info(f"Order fetched successfully: {order}")
            return OrderInDB(**order)

        except Exception as e:
            logger.error(f"Error occurred while fetching order: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred." + str(e))

    async def update_order(self, order_id: str, update_data: OrderUpdate):
        try:
            obj_id = ObjectId(order_id)
            logger.info(f"Updating order with ID: {order_id}")
        except Exception:
            logger.error(f"Invalid ObjectId provided for update: {order_id}")
            raise HTTPException(status_code=400, detail="Invalid ObjectId provided.")

        update_data_dict = update_data.dict(exclude_unset=True)
        if update_data_dict:
            update_data_dict['updated_at'] = datetime.utcnow()

        try:
            result = await self.db.orders.update_one({"_id": obj_id}, {"$set": update_data_dict})

            if result.modified_count == 0:
                logger.warning(f"No modifications made or order not found with ID: {order_id}")
                raise HTTPException(status_code=404, detail="Order NOT found or no changes made.")

            logger.info(f"Order updated successfully. Fetching updated order.")
            updated_order = await self.get_order(order_id)
            return updated_order

        except Exception as e:
            logger.error(f"Error occurred during order update: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error updating order: {str(e)}")

    async def delete_order(self, order_id: str):
        try:
            obj_id = ObjectId(order_id)
            logger.info(f"Deleting order with ID: {order_id}")
        except Exception:
            logger.error(f"Invalid ObjectId provided for deletion: {order_id}")
            raise HTTPException(status_code=400, detail="Invalid ObjectId provided.")

        try:
            result = await self.db.orders.delete_one({"_id": obj_id})

            if result.deleted_count == 0:
                logger.warning(f"Order not found with ID: {order_id}")
                raise HTTPException(status_code=404, detail="Order NOT found.")
            logger.info(f"Order with ID {order_id} deleted successfully.")
            return {"detail": "Order deleted successfully."}

        except Exception as e:
            logger.error(f"Error occurred while deleting order: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error deleting order: {str(e)}")