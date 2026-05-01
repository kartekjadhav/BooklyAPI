# Bookly

Bookly is a FastAPI-based REST API for a book review platform. It provides user authentication, email verification, password reset, JWT-based access control, book management, review management, PostgreSQL persistence, Redis-backed token revocation, Alembic migrations, and Celery-powered background email delivery.

## Features

- User signup, login, logout, profile lookup, email verification, and password reset
- JWT access and refresh tokens with Redis-backed token blocklisting
- Role-based authorization for verified users and administrators
- CRUD operations for books
- CRUD operations for book reviews
- SQLModel models backed by PostgreSQL through SQLAlchemy async sessions
- Alembic database migrations
- FastAPI-Mail integration for transactional email
- Celery worker support with Redis as broker/result backend
- Centralized exception handling with consistent JSON error responses
- Pytest-based test suite structure

## Tech Stack

- **Python**: 3.12
- **API framework**: FastAPI
- **Database**: PostgreSQL
- **ORM / data models**: SQLModel, SQLAlchemy async
- **Migrations**: Alembic
- **Cache / token blocklist**: Redis
- **Background jobs**: Celery
- **Email**: FastAPI-Mail
- **Validation / settings**: Pydantic v2, Pydantic Settings
- **Testing**: Pytest, FastAPI TestClient
- **Package management**: uv / pip-compatible requirements

## Project Structure

```text
Bookly/
|-- main.py                         # Local development entry point
|-- pyproject.toml                  # Project metadata, dependencies, pytest config
|-- requirements.txt                # Pip-compatible dependency list
|-- alembic.ini                     # Alembic configuration
|-- migrations/                     # Database migration environment and revisions
|   |-- env.py
|   `-- versions/
|-- src/
|   |-- app.py                      # FastAPI app factory-style module, routers, lifespan
|   |-- book_data.py                # Legacy/sample book data
|   |-- celery_app.py               # Celery application and email task
|   |-- mail.py                     # FastAPI-Mail configuration and message creation
|   |-- middleware.py               # Application middleware registration
|   |-- db/
|   |   `-- db.py                   # Async database engine and session dependency
|   |-- dependencies/
|   |   |-- bearer.py               # JWT bearer token validation dependencies
|   |   |-- get_current_user.py     # Current-user dependency
|   |   `-- role_checker.py         # Role and verification checks
|   |-- email_templates/            # HTML email template generators
|   |-- errors/
|   |   `-- errors.py               # Custom exceptions and exception handlers
|   |-- models/
|   |   `-- all_models.py           # SQLModel database models
|   |-- redis/
|   |   `-- redis.py                # Redis client and JWT blocklist helpers
|   |-- routes/
|   |   |-- auth_router.py          # Authentication and account endpoints
|   |   |-- book_router.py          # Book endpoints
|   |   `-- review_router.py        # Review endpoints
|   |-- schemas/
|   |   |-- BookSchemas.py          # Book request/response schemas
|   |   |-- UserSchemas.py          # User request/response schemas
|   |   |-- review_schemas.py       # Review request/response schemas
|   |   |-- setting.py              # Environment-backed application settings
|   |   `-- token.py                # JWT payload typing
|   |-- services/
|   |   |-- book_service.py         # Book business logic
|   |   |-- review_service.py       # Review business logic
|   |   `-- user_service.py         # User business logic
|   `-- utils/
|       |-- jwtUtil.py              # JWT generation and verification
|       |-- passwdUtil.py           # Password hashing and verification
|       `-- token_util.py           # Timed serializer tokens for email flows
`-- tests/
    |-- conftest.py                 # Test fixtures and dependency overrides
    |-- test_auth.py
    `-- test_book.py
```

## Architecture Overview

Bookly follows a layered API architecture:

1. **Routes** receive HTTP requests, validate request bodies with Pydantic schemas, and declare dependencies such as database sessions, authentication, and role checks.
2. **Dependencies** handle cross-cutting request concerns, including bearer token validation, current-user lookup, and role/verification enforcement.
3. **Services** contain the core business logic for users, books, and reviews.
4. **Models** define the database tables using SQLModel.
5. **Schemas** define request and response contracts.
6. **Infrastructure modules** configure PostgreSQL, Redis, Celery, email, middleware, and application-level errors.

The application starts in `src.app:app`. During the FastAPI lifespan startup, it verifies PostgreSQL connectivity and retries Redis connectivity before serving requests.

## Prerequisites

Install and run the following before starting the API:

- Python 3.12
- PostgreSQL
- Redis
- uv or pip

## Environment Variables

Create a `.env` file in the project root. The application reads it through `src/schemas/setting.py`.

```env
DOMAIN=127.0.0.1:8000
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/bookly
JWT_SECRET=replace-with-a-secure-secret
JWT_ALGORITHM=HS256
REDIS_URL=redis://localhost:6379
REDIS_PORT=6379

MAIL_USERNAME=your-email-username
MAIL_PASSWORD=your-email-password
MAIL_FROM=noreply@example.com
MAIL_PORT=587
MAIL_SERVER=smtp.example.com
MAIL_FROM_NAME=Bookly
MAIL_STARTTLS=true
MAIL_SSL_TLS=false
USE_CREDENTIALS=true
VALIDATE_CERTS=true

ITSDANGEROUS_SECRET_KEY=replace-with-a-secure-token-secret
```

> Do not commit real secrets. Keep production credentials in a secure secret manager or deployment environment.

## Installation

### Using uv

```bash
uv sync
```

### Using pip

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux, activate the virtual environment with:

```bash
source .venv/bin/activate
```

## Database Setup

Ensure PostgreSQL is running and that `DATABASE_URL` points to an existing database.

Apply migrations:

```bash
alembic upgrade head
```

Create a new migration after model changes:

```bash
alembic revision --autogenerate -m "describe change"
```

## Running the Application

Start the API with:

```bash
python main.py
```

Or run Uvicorn directly:

```bash
uvicorn src.app:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at:

- API base URL: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Running Redis

Redis is required for:

- JWT logout/blocklist support
- Celery broker and result backend

The default Redis URL is:

```text
redis://localhost:6379
```

## Running Celery

Start the Celery worker:

```bash
celery -A src.celery_app:celery_app worker --pool=solo --loglevel=info
```

Start Flower for worker monitoring:

```bash
celery -A src.celery_app:celery_app flower --port=5555
```

Flower will be available at:

```text
http://localhost:5555
```

## Authentication

Bookly uses JWT bearer authentication.

After login, the API returns:

- `access_token`: used in the `Authorization` header
- `refresh_token`: used to request a new access token

Send authenticated requests with:

```http
Authorization: Bearer <access_token>
```

Most book and review endpoints require:

- A valid access token
- A non-revoked token
- A verified account
- A role allowed by the endpoint

## API Reference

Base path:

```text
/api/v1
```

### Auth Endpoints

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| `POST` | `/auth/signup` | Public | Create a user account and send verification email |
| `GET` | `/auth/verify_email/{token}` | Public | Verify a user's email address |
| `POST` | `/auth/login` | Public | Authenticate user and return access/refresh tokens |
| `GET` | `/auth/me` | Access token | Return current user details with books |
| `GET` | `/auth/refresh` | Refresh token | Issue a new access token |
| `GET` | `/auth/logout` | Access token | Revoke the current access token |
| `POST` | `/auth/send_email` | Public | Send a test email through the background email task |
| `POST` | `/auth/reset_password` | Public | Send password reset instructions |
| `POST` | `/auth/reset_password_confirm/{token}` | Public | Reset password with a valid reset token |

#### Signup Request

```json
{
  "username": "reader123",
  "first_name": "Reader",
  "last_name": "One",
  "password": "secret123",
  "email": "reader@example.com"
}
```

#### Login Request

```json
{
  "email": "reader@example.com",
  "password": "secret123"
}
```

#### Login Response

```json
{
  "message": "Login Successfull",
  "access_token": "<jwt-access-token>",
  "refresh_token": "<jwt-refresh-token>",
  "user": {
    "uid": "user-uuid",
    "email": "reader@example.com"
  }
}
```

#### Password Reset Request

```json
{
  "email": "reader@example.com"
}
```

#### Password Reset Confirmation Request

```json
{
  "new_password": "newsecret123",
  "confirm_password": "newsecret123"
}
```

### Book Endpoints

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| `GET` | `/books/` | Access token | List all books |
| `GET` | `/books/{book_uid}` | Access token | Get one book with its reviews |
| `POST` | `/books/` | Access token | Create a book owned by the current user |
| `PATCH` | `/books/{book_uid}` | Access token | Partially update a book |
| `DELETE` | `/books/{book_uid}` | Access token | Delete a book |

#### Create Book Request

```json
{
  "title": "Clean Architecture",
  "author": "Robert C. Martin",
  "publisher": "Pearson",
  "publish_date": "2017-09-20",
  "page_count": 432,
  "language": "English"
}
```

#### Update Book Request

All fields are optional.

```json
{
  "author": "Robert C. Martin",
  "publisher": "Pearson",
  "publish_date": "2017-09-20",
  "page_count": 432,
  "language": "English"
}
```

#### Book Response Shape

```json
{
  "uid": "book-uuid",
  "user_uid": "user-uuid",
  "title": "Clean Architecture",
  "author": "Robert C. Martin",
  "publisher": "Pearson",
  "publish_date": "2017-09-20",
  "page_count": 432,
  "language": "English",
  "created_at": "2026-05-01T08:00:00Z",
  "updated_at": "2026-05-01T08:00:00Z"
}
```

### Review Endpoints

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| `GET` | `/reviews/` | Access token | List all reviews |
| `GET` | `/reviews/{review_uid}` | Access token | Get one review |
| `POST` | `/reviews/book/{book_uid}` | Access token | Add a review to a book |
| `PATCH` | `/reviews/{review_uid}` | Access token | Update a review |
| `DELETE` | `/reviews/{review_uid}` | Access token | Delete a review |

#### Create Review Request

```json
{
  "rating": 5,
  "review_text": "A practical and thoughtful guide to software architecture."
}
```

#### Update Review Request

```json
{
  "rating": 4,
  "review_text": "Still excellent, with a few sections that require careful reading."
}
```

#### Review Response Shape

```json
{
  "uid": "review-uuid",
  "user_uid": "user-uuid",
  "book_uid": "book-uuid",
  "review_text": "A practical and thoughtful guide to software architecture.",
  "rating": 5,
  "created_at": "2026-05-01T08:00:00Z",
  "updated_at": "2026-05-01T08:00:00Z"
}
```

## Data Model

### Users

Stores account and authentication-related fields.

- `uid`
- `username`
- `password_hash`
- `first_name`
- `last_name`
- `email`
- `role`
- `verified`
- `created_at`
- `updated_at`

Relationships:

- One user can create many books.
- One user can create many reviews.

### Books

Stores book catalog data.

- `uid`
- `title`
- `author`
- `publisher`
- `publish_date`
- `page_count`
- `language`
- `user_uid`
- `created_at`
- `updated_at`

Relationships:

- Each book belongs to one user.
- Each book can have many reviews.

### Reviews

Stores user reviews for books.

- `uid`
- `user_uid`
- `book_uid`
- `review_text`
- `rating`
- `created_at`
- `updated_at`

Relationships:

- Each review belongs to one user.
- Each review belongs to one book.

## Error Responses

The API registers custom handlers for domain errors and returns consistent JSON error bodies.

Common errors include:

| Error | HTTP Status | Error Code |
| --- | ---: | --- |
| Account not verified | `403` | `account_not_verified` |
| Invalid credentials | `401` | `invalid_credentials` |
| Invalid or expired token | `401` | `invalid_token` |
| Invalid or revoked token | `401` | `invalid_or_revoked_token` |
| Insufficient privileges | `403` | `insufficient_privileges` |
| User already exists | `409` | `user_already_exists` |
| User not found | `404` | `user_not_found` |
| Book already exists | `409` | `book_already_exists` |
| Book not found | `404` | `book_not_found` |
| Review not found | `404` | `review_not_found` |
| Internal server error | `500` | `internal_server_error` |

Example:

```json
{
  "message": "Book not found",
  "error_code": "book_not_found"
}
```

## Testing

Run the test suite with:

```bash
pytest
```

The pytest configuration in `pyproject.toml` sets:

- `pythonpath = ["src"]`
- `testpaths = ["tests"]`
- warning filters for deprecation-related warnings

## Development Workflow

Recommended local workflow:

1. Start PostgreSQL.
2. Start Redis.
3. Create or update `.env`.
4. Install dependencies.
5. Run `alembic upgrade head`.
6. Start the FastAPI app.
7. Start the Celery worker if testing email flows.
8. Use `/docs` to exercise endpoints interactively.
9. Run `pytest` before submitting changes.

## Security Notes

- Passwords are stored as hashes, not plain text.
- Access and refresh tokens are signed with `JWT_SECRET`.
- Logged-out access tokens are blocklisted in Redis by JWT ID.
- Email verification and password reset links use timed serializer tokens.
- Protected routes require verified accounts through `RoleChecker`.

For production deployments:

- Use strong, unique secrets.
- Use TLS for public traffic.
- Use managed secret storage instead of local `.env` files.
- Restrict database and Redis network access.
- Configure trusted SMTP credentials.
- Set appropriate CORS policy in middleware.

## Useful Commands

```bash
# Run API
python main.py

# Run API with Uvicorn
uvicorn src.app:app --reload

# Apply migrations
alembic upgrade head

# Generate migration
alembic revision --autogenerate -m "migration message"

# Run tests
pytest

# Start Celery worker
celery -A src.celery_app:celery_app worker --pool=solo --loglevel=info

# Start Flower
celery -A src.celery_app:celery_app flower --port=5555
```

## License

No license file is currently included. Add a license before distributing or publishing this project.
