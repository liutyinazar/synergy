# User Data Collection Application

A FastAPI application that periodically collects and stores user data using various APIs.

## Technologies Used

- FastAPI
- Celery
- MongoDB
- Redis
- Docker
- pytest

## Requirements

- Docker
- Docker Compose

## Installation and Running

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Run with Docker Compose:
```bash
docker-compose up -d
```

The application will be available at http://localhost:8000

## API Endpoints

### Users

#### GET /users/
Returns a list of all users.

Response:
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

#### GET /users/{user_id}
Returns a specific user by ID.

Response:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Addresses

#### GET /users/{user_id}/address
Returns the address for a specific user.

Response:
```json
{
  "street": "123 Main St",
  "city": "New York",
  "state": "NY",
  "zip_code": "10001",
  "user_id": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Credit Cards

#### GET /users/{user_id}/credit-card
Returns the credit card for a specific user.

Response:
```json
{
  "type": "Visa",
  "number": "1234567890",
  "expiration": "01/25",
  "owner": "John Doe",
  "user_id": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

## Celery Tasks

The application includes three periodic tasks:

1. `fetch_users`: Fetches user data every 1 minute
2. `fetch_addresses`: Fetches address data every 2 minutes
3. `fetch_credit_cards`: Fetches credit card data every 3 minutes

## Testing

### Running Tests Locally

1. Install development dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest app/tests/test_api.py

# Run tests with verbose output
pytest -v
```

### Running Tests in Docker

```bash
# Run tests in the application container
docker-compose exec app pytest

# Run tests with coverage in the application container
docker-compose exec app pytest --cov=app
```

## Code Quality

The project uses several tools to maintain code quality:

- **Black**: Code formatting
- **Flake8**: Code linting
- **isort**: Import sorting
- **mypy**: Type checking

Run all code quality checks:
```bash
# Format code
black .

# Check code style
flake8

# Sort imports
isort .

# Check types
mypy .
```

## Deployment on AWS

The project includes Terraform configuration for deploying to AWS. See the `terraform` directory for details.

## Project Structure

```
.
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── tasks/
│   └── tests/
├── docker/
├── terraform/
├── docker-compose.yml
├── Dockerfile
└── README.md
``` 