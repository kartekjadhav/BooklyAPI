from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from src.routes import book_router, auth_router, review_router
from contextlib import asynccontextmanager
from src.db.db import init_db
from src.redis.redis import token_blocklist
from src.errors.errors import register_all_errors
from .middleware import register_middlewares
from rich.console import Console


REDIS_CONNECTION_RETRIES = 6
console = Console()


@asynccontextmanager
async def life_span(app:FastAPI):
    console.print("[bold green]Server is starting 🟢[/bold green]")

    # Check Postgres DB connectivity
    await init_db()

    # Check redis connectivity
    for try_attempt in range(REDIS_CONNECTION_RETRIES):
        try:
            redis_connection = await token_blocklist.ping()
            if redis_connection:
                console.print("[green]✅ Redis connection working fine[/green]")
                break
        except Exception as e:
            if try_attempt == REDIS_CONNECTION_RETRIES - 1:
                console.print("[red]❌ Redis connection failed[/red]", style="bold")
                raise Exception("❌ Redis connection not working")
            else:
                console.print(f"[yellow]Couldn't establish Redis connection, retrying ({try_attempt+1}/{REDIS_CONNECTION_RETRIES-1})[/yellow]")
    yield
    console.print("[bold red]Server is stopping 🔴[/bold red]")

app = FastAPI(lifespan=life_span, title="Bookly", description="A REST API for book review web service", version="v1")
   
register_all_errors(app)
register_middlewares(app)

# User auth Router
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

# Book Router
app.include_router(book_router, prefix="/api/v1/books", tags=["books"])

# Review Router
app.include_router(review_router, prefix="/api/v1/reviews", tags=["review"])

