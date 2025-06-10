# User Data Collection Application

A FastAPI application that periodically collects and stores user data using various APIs.

## Technologies Used

- FastAPI
- Celery
- MongoDB
- Redis
- Docker
- pytest
- Terraform (AWS)

## Requirements

- Docker
- Docker Compose
- AWS CLI (for deployment)
- Terraform (for deployment)

## Environment Configuration

The application uses environment variables for configuration. Create the following files:

1. `.env` for production:
```bash
MONGODB_URL=mongodb://mongodb:27017
REDIS_URL=redis://redis:6379/0
API_BASE_URL=https://fakerapi.it/api/v2
DATABASE_NAME=user_data_db
```

2. `.env.test` for testing:
```bash
MONGODB_URL=mongodb://mongodb:27017
REDIS_URL=redis://redis:6379/0
API_BASE_URL=https://fakerapi.it/api/v2
DATABASE_NAME=user_data_db_test
TESTING=true
```

3. `.env.example` (template for other developers):
```bash
MONGODB_URL=mongodb://mongodb:27017
REDIS_URL=redis://redis:6379/0
API_BASE_URL=https://fakerapi.it/api/v2
DATABASE_NAME=user_data_db
```

Note: 
- `.env` and `.env.test` should be added to `.gitignore`
- `.env.example` should be committed to the repository
- For local development, copy `.env.example` to `.env`
- For testing, copy `.env.example` to `.env.test`

## Installation and Running

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create environment files:
```bash
cp .env.example .env
cp .env.example .env.test
```

3. Run with Docker Compose:
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
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "firstname": "John",
    "lastname": "Doe",
    "username": "johndoe",
    "email": "john@example.com",
    "ip": "192.168.1.1",
    "macAddress": "00:1B:44:11:3A:B7",
    "website": "johndoe.com",
    "image": "https://example.com/image.jpg",
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
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "firstname": "John",
  "lastname": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "ip": "192.168.1.1",
  "macAddress": "00:1B:44:11:3A:B7",
  "website": "johndoe.com",
  "image": "https://example.com/image.jpg",
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

## Logging

The application logs are stored in the following locations:

- Application logs: `logs/app.log`
- Linter logs:
  - `logs/flake8.log`
  - `logs/isort.log`
  - `logs/mypy.log`
- Test logs: `logs/tests/pytest.log`

Logs are automatically mounted to the host machine in the `./logs` directory.

## Celery Tasks

The application includes three periodic tasks:

1. `fetch_users`: Fetches user data every 1 minute
2. `fetch_addresses`: Fetches address data every 2 minutes
3. `fetch_credit_cards`: Fetches credit card data every 3 minutes

## Testing

### Running Tests

You can run tests using the provided script:
```bash
./run_tests.sh
```

This will:
1. Run all tests using pytest
2. Save test results to `logs/tests/pytest.log`
3. Show overall test status

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

### Running All Linters

You can run all linters at once using the provided script:
```bash
./check_linters.sh
```

This will:
1. Run all linters (flake8, isort, mypy)
2. Save results to the `logs` directory
3. Show overall status for each linter

The logs will be available in:
- `logs/flake8.log`
- `logs/isort.log`
- `logs/mypy.log`

## Deployment on AWS

The project includes Terraform configuration for deploying to AWS. See the `terraform` directory for details.

### Deployment Steps

1. Configure AWS credentials:
```bash
aws configure
```

2. Initialize Terraform:
```bash
cd terraform
terraform init
```

3. Apply the configuration:
```bash
terraform apply
```

4. After deployment, SSH into the instance:
```bash
ssh -i /path/to/synergy-key.pem ubuntu@<instance-public-ip>
```

5. Clone your repository and start the application:
```bash
git clone <your-repo-url>
cd <your-repo>
docker-compose up -d
```

### Cleanup

To destroy the infrastructure:
```bash
terraform destroy
```

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
├── logs/
│   ├── app.log
│   ├── flake8.log
│   ├── isort.log
│   ├── mypy.log
│   └── tests/
│       └── pytest.log
├── docker-compose.yml
├── Dockerfile
├── check_linters.sh
├── run_tests.sh
└── README.md
``` 