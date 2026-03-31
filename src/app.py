from fastapi import FastAPI
from src.routes import book_router, auth_router
from contextlib import asynccontextmanager
from src.db.db import init_db
from src.redis.redis import token_blocklist

REDIS_CONNECTION_RETRIES = 6


@asynccontextmanager
async def life_span(app:FastAPI):
    print("Server is starting 🟢")

    # Check Postgres DB connectivity
    await init_db()

    # Check redis connectivity
    for try_attempt in range(REDIS_CONNECTION_RETRIES):
        try:
            redis_connection = await token_blocklist.ping()
            if redis_connection:
                print("✅ Redis connection working fine")
                break
        except Exception as e:
            if try_attempt == REDIS_CONNECTION_RETRIES - 1:
                print("❌ Redis connection failed")
                raise Exception("❌ Redis connection not working")  # crash app
            else:
                print(f"Couldn't establish Redis connection, retrying again (attempt - {try_attempt+1} / {REDIS_CONNECTION_RETRIES-1})")
    yield
    print("Server is stopping 🔴")

app = FastAPI(lifespan=life_span, title="Bookly", description="A REST API for book review web service", version="v1")

# User auth Router
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

# Book Router
app.include_router(book_router, prefix="/api/v1/books", tags=["books"])