import pytest
from unittest.mock import AsyncMock, patch
from app.tasks.user import fetch_users
from app.tasks.address import fetch_addresses
from app.tasks.credit_card import fetch_credit_cards


@pytest.mark.asyncio
async def test_fetch_users():
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = AsyncMock(
            status_code=200,
            json=lambda: {
                "data": [
                    {
                        "id": 1,
                        "uuid": "test-uuid",
                        "firstname": "John",
                        "lastname": "Doe",
                        "username": "johndoe",
                        "email": "test@example.com",
                        "ip": "192.168.1.1",
                        "macAddress": "00:11:22:33:44:55",
                        "website": "https://example.com",
                        "image": "https://example.com/image.jpg",
                    }
                ]
            },
        )

        with patch("motor.motor_asyncio.AsyncIOMotorClient") as mock_mongo:
            mock_db = AsyncMock()
            mock_mongo.return_value.__getitem__.return_value = mock_db
            mock_db.users.insert_one = AsyncMock()

            result = fetch_users.delay()
            assert result.get()["status"] == "success"
            assert "Fetched" in result.get()["message"]


@pytest.mark.asyncio
async def test_fetch_addresses():
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = AsyncMock(
            status_code=200,
            json=lambda: {
                "data": [
                    {
                        "id": 1,
                        "street": "Test Street",
                        "streetName": "Test Street Name",
                        "buildingNumber": "123",
                        "city": "Test City",
                        "zipcode": "12345",
                        "country": "Test Country",
                        "country_code": "TC",
                        "latitude": 12.34,
                        "longitude": 56.78,
                    }
                ]
            },
        )

        with patch("motor.motor_asyncio.AsyncIOMotorClient") as mock_mongo:
            mock_db = AsyncMock()
            mock_mongo.return_value.__getitem__.return_value = mock_db
            mock_db.users.find = AsyncMock(
                return_value=AsyncMock(to_list=AsyncMock(return_value=[{"id": 1}]))
            )
            mock_db.addresses.insert_one = AsyncMock()

            result = fetch_addresses.delay()
            assert result.get()["status"] == "success"
            assert "Fetched" in result.get()["message"]


@pytest.mark.asyncio
async def test_fetch_credit_cards():
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = AsyncMock(
            status_code=200,
            json=lambda: {
                "data": [
                    {
                        "type": "Visa",
                        "number": "1234567890",
                        "expiration": "01/25",
                        "owner": "Test Owner",
                    }
                ]
            },
        )

        with patch("motor.motor_asyncio.AsyncIOMotorClient") as mock_mongo:
            mock_db = AsyncMock()
            mock_mongo.return_value.__getitem__.return_value = mock_db
            mock_db.users.find = AsyncMock(
                return_value=AsyncMock(to_list=AsyncMock(return_value=[{"id": 1}]))
            )
            mock_db.credit_cards.update_one = AsyncMock()

            result = fetch_credit_cards.delay()
            assert result.get()["status"] == "success"
            assert "Fetched" in result.get()["message"]
