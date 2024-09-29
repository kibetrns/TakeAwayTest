import logging
from app.api.models.customer_model import CustomerInDB, CustomerUpdate
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from pymongo import errors

logger = logging.getLogger(__name__)

class CustomerService:
    def __init__(self, db):
        self.db = db

    async def create_customer(self, customer_data):
        customer_data['created_at'] = datetime.utcnow()
        try:
            logger.info(f"Creating new customer with data: {customer_data}")
            result = await self.db.customers.insert_one(customer_data)
            customer_id = result.inserted_id
            customer_data.pop('_id', None)
            logger.info(f"Customer created successfully with ID: {customer_id}")
            return CustomerInDB(**customer_data, _id=str(customer_id))
        except errors.DuplicateKeyError:
            logger.error(f"Duplicate key error for email: {customer_data.get('email_address')}")
            raise HTTPException(status_code=400, detail="Email address already exists.")
        except Exception as e:
            logger.error(f"Error occurred while creating customer: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    async def get_customer(self, customer_id: str):
        try:
            obj_id = ObjectId(customer_id)
            logger.info(f"Fetching customer with ID: {customer_id}")
        except Exception:
            logger.error(f"Invalid ObjectId provided: {customer_id}")
            raise HTTPException(status_code=400, detail="Provide a valid ObjectId. The one you've provided is NOT valid.")

        customer = await self.db.customers.find_one({"_id": obj_id})

        if customer is None:
            logger.warning(f"Customer with ID {customer_id} not found.")
            raise HTTPException(status_code=404, detail="Customer NOT found.")

        customer["_id"] = str(customer["_id"])
        logger.info(f"Customer fetched successfully: {customer}")
        return CustomerInDB(**customer)


    async def update_customer(self, customer_id: str, update_data: CustomerUpdate):
        try:
            obj_id = ObjectId(customer_id)
            logger.info(f"Updating customer with ID: {customer_id}")
        except Exception:
            logger.error(f"Invalid ObjectId provided for update: {customer_id}")
            raise HTTPException(status_code=400, detail="Invalid ObjectId provided for update.")


        update_data_dict = update_data.dict(exclude_unset=True)

        if update_data_dict:
            update_data_dict['updated_at'] = datetime.utcnow()

        try:
            existing_customer = await self.db.customers.find_one({"_id": obj_id})
            if not existing_customer:
                logger.warning(f"Customer with ID: {customer_id} NOT found.")
                raise HTTPException(status_code=404, detail=f"Customer with ID: {customer_id} NOT found.")

            logger.info(f"Current customer data: {existing_customer}")

            new_email = update_data_dict.get("email_address")
            current_email = existing_customer.get("email_address")

            logger.info(f"New email: {new_email}, Current email: {current_email}")

            if new_email and new_email != current_email:

                email_exists = await self.db.customers.find_one({"email_address": new_email})
                logger.info(f"Email exists in database: {email_exists is not None}")

                if email_exists:
                    logger.error(f"Duplicate email address detected: {new_email}")
                    raise HTTPException(status_code=400, detail="Email address already exists.")

            if update_data_dict:
                result = await self.db.customers.update_one({"_id": obj_id}, {"$set": update_data_dict})

                if result.modified_count == 0:
                    logger.warning(f"No modifications made or customer not found with ID: {customer_id}")
                    raise HTTPException(status_code=404, detail="Customer NOT found or no changes made.")

                logger.info(f"Customer updated successfully. Fetching updated customer.")
                updated_customer = await self.get_customer(customer_id)
                return updated_customer
            else:
                logger.info(f"No changes to update for customer ID: {customer_id}")
                return await self.get_customer(customer_id)

        except Exception as e:
            logger.error(f"Error occurred during customer update: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error updating customer: {str(e)}")

    async def delete_customer(self, customer_id: str):
        try:
            obj_id = ObjectId(customer_id) 
            logger.info(f"Deleting customer with ID: {customer_id}")
        except Exception:
            logger.error(f"Provide a valid customer_id which is of type ObjectId. The one you provided ({customer_id}) is NOT valid.")
            raise HTTPException(status_code=400, detail=f"Provide a valid customer_id which is of type ObjectId. The one you've provided ({customer_id}) is NOT valid.")

        try:
            result = await self.db.customers.delete_one({"_id": obj_id})

            if result.deleted_count == 0:
                logger.warning(f"Customer not found with ID: {customer_id}")
                raise HTTPException(status_code=404, detail="Customer NOT found.")

            logger.info(f"Customer deleted successfully with ID: {customer_id}")
            return {"detail": "Customer deleted successfully."}

        except Exception as e:
            logger.error(f"Error occurred while deleting customer: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))