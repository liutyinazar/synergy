from datetime import UTC, datetime
from typing import Any, Dict

from app.models.address import Address
from app.models.credit_card import CreditCard
from app.models.user import User


def test_user_model() -> None:
    user_data: Dict[str, Any] = {
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
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
    }
    user = User(**user_data)
    assert user.id == user_data["id"]
    assert user.uuid == user_data["uuid"]
    assert user.firstname == user_data["firstname"]
    assert user.lastname == user_data["lastname"]
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]


def test_address_model() -> None:
    address_data: Dict[str, Any] = {
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
        "user_id": 1,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
    }
    address = Address(**address_data)
    assert address.id == address_data["id"]
    assert address.street == address_data["street"]
    assert address.streetName == address_data["streetName"]
    assert address.buildingNumber == address_data["buildingNumber"]
    assert address.city == address_data["city"]
    assert address.zipcode == address_data["zipcode"]
    assert address.country == address_data["country"]
    assert address.country_code == address_data["country_code"]
    assert address.latitude == address_data["latitude"]
    assert address.longitude == address_data["longitude"]
    assert address.user_id == address_data["user_id"]


def test_credit_card_model() -> None:
    credit_card_data: Dict[str, Any] = {
        "type": "Visa",
        "number": "1234567890",
        "expiration": "01/25",
        "owner": "Test Owner",
        "user_id": 1,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
    }
    credit_card = CreditCard(**credit_card_data)
    assert credit_card.type == credit_card_data["type"]
    assert credit_card.number == credit_card_data["number"]
    assert credit_card.expiration == credit_card_data["expiration"]
    assert credit_card.owner == credit_card_data["owner"]
    assert credit_card.user_id == credit_card_data["user_id"]
