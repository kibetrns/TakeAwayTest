import pytest
from fastapi import HTTPException
from app.api.models.customer_model import CustomerInDB, CustomerUpdate
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from app.api.services.customer_service import CustomerService
from unittest.mock import AsyncMock, MagicMock
from bson import ObjectId

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def customer_service(mock_db):
    return CustomerService(mock_db)

def sample_customer_data():
    return {
        "full_name": "Jaba Ganji",
        "email_address": "ganji@jaba.com",
        "phone_number": "+254791111111",
        "created_at": datetime.utcnow(),
    }


@pytest.mark.asyncio
async def test_create_customer_success(customer_service, mock_db):
    customer_data = sample_customer_data()

    mock_db.customers.insert_one = AsyncMock(return_value=MagicMock(inserted_id=ObjectId()))

    result = await customer_service.create_customer(customer_data)

    assert isinstance(result, CustomerInDB)
    assert result.email_address == customer_data['email_address']
    assert mock_db.customers.insert_one.called

@pytest.mark.asyncio
async def test_create_customer_duplicate_email(customer_service, mock_db):
    customer_data = sample_customer_data()

    mock_db.customers.insert_one = AsyncMock(side_effect=DuplicateKeyError("Duplicate email"))

    with pytest.raises(HTTPException) as exc_info:
        await customer_service.create_customer(customer_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Email address already exists."

@pytest.mark.asyncio
async def test_get_customer_success(customer_service, mock_db):
    customer_id = str(ObjectId())

    mock_db.customers.find_one = AsyncMock(return_value={
        "_id": ObjectId(customer_id),
        "full_name": "Ganji Doe",
        "email_address": "john@example.com",
        "phone_number": "+254791111111",
        "created_at": datetime.utcnow(),
    })

    result = await customer_service.get_customer(customer_id)

    assert isinstance(result, CustomerInDB)
    assert result.email_address == "john@example.com"
    assert mock_db.customers.find_one.called


@pytest.mark.asyncio
async def test_get_customer_not_found(customer_service, mock_db):
    customer_id = str(ObjectId())

    mock_db.customers.find_one = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await customer_service.get_customer(customer_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Customer NOT found."

"""
@pytest.mark.asyncio
async def test_update_customer_success(customer_service, mock_db):
    customer_id = str(ObjectId())

    existing_customer_data = {
        "_id": ObjectId(customer_id),
        "email_address": "old_email@example.com",
        "full_name": "Past Gandi",
        "phone_number": "+1234567890",
        "created_at": datetime.utcnow()
    }

    mock_db.customers.find_one = AsyncMock(side_effect=lambda query: existing_customer_data if query.get("_id") == existing_customer_data["_id"] else None)

    async def mock_check_email(query):
        if query.get("email_address") == "new_email@example.com":
            return None
        return existing_customer_data

    mock_db.customers.find_one = AsyncMock(side_effect=mock_check_email)

    mock_update_result = MagicMock(modified_count=1)

    async def update_one_and_return_updated_customer(query, update):
        return mock_update_result

    mock_db.customers.update_one = AsyncMock(side_effect=update_one_and_return_updated_customer)

    update_data = CustomerUpdate(email_address="new_email@example.com")

    result = await customer_service.update_customer(customer_id, update_data)

    assert result.email_address == "new_email@example.com"

    assert mock_db.customers.find_one.call_count == 2
"""


"""
@pytest.mark.asyncio
async def test_update_customer_not_found(customer_service, mock_db):
    customer_id = str(ObjectId())
    update_data = CustomerUpdate(email_address="new_email@example.com")

    mock_db.customers.find_one = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await customer_service.update_customer(customer_id, update_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Customer with ID: {customer_id} NOT found."

"""

@pytest.mark.asyncio
async def test_delete_customer_success(customer_service, mock_db):
    customer_id = str(ObjectId())

    mock_db.customers.delete_one = AsyncMock(return_value=MagicMock(deleted_count=1))

    result = await customer_service.delete_customer(customer_id)

    assert result == {"detail": "Customer deleted successfully."}
    assert mock_db.customers.delete_one.called

@pytest.mark.asyncio
async def test_delete_customer_success(customer_service, mock_db):
    customer_id = str(ObjectId())

    mock_db.customers.delete_one = AsyncMock(return_value=MagicMock(deleted_count=1))

    response = await customer_service.delete_customer(customer_id)

    assert response == {"detail": "Customer deleted successfully."}

@pytest.mark.asyncio
async def test_delete_customer_invalid_id(customer_service, mock_db):
    customer_id = "invalid_id"

    with pytest.raises(HTTPException) as exc_info:
        await customer_service.delete_customer(customer_id)

    assert exc_info.value.status_code == 400
    assert "valid customer_id" in exc_info.value.detail


"""
@pytest.mark.asyncio
async def test_delete_customer_not_found(customer_service, mock_db):
    customer_id = str(ObjectId())

    mock_db.customers.delete_one = AsyncMock(return_value=MagicMock(deleted_count=0))

    with pytest.raises(HTTPException) as exc_info:
        await customer_service.delete_customer(customer_id)

    assert exc_info.value.status_code == 404
    assert "Customer NOT found" in exc_info.value.detail

 """


@pytest.mark.asyncio
async def test_delete_customer_unexpected_error(customer_service, mock_db):
    customer_id = str(ObjectId())

    mock_db.customers.delete_one = AsyncMock(side_effect=Exception("Unexpected database error"))

    with pytest.raises(HTTPException) as exc_info:
        await customer_service.delete_customer(customer_id)

    assert exc_info.value.status_code == 500
    assert "An unexpected error occurred" in exc_info.value.detail