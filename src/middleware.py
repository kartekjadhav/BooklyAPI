import os
import time
import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware 
from rich.console import Console

console = Console()

logger = logging.getLogger("uvicorn.access")
logger.disabled = True
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000"  # If you have a frontend
]
def register_middlewares(app: FastAPI):

    @app.middleware('http')
    async def custom_request_logging(request: Request, call_next):


        start_time = time.time()

        response = await call_next(request)

        end_time = time.time()
        total_processing_time = end_time - start_time

        # Determine status color
        if response.status_code < 300:
            status_color = "green"
        elif response.status_code < 400:
            status_color = "yellow"
        else:
            status_color = "red"

        # Determine method color
        method_colors = {
            "GET": "cyan",
            "POST": "green",
            "PUT": "yellow",
            "DELETE": "red",
            "PATCH": "magenta"
        }
        method_color = method_colors.get(request.method, "white")

        console.print(
            f"[dim]CLIENT[/dim] [blue]{request.client.host}:{request.client.port}[/blue] "
            f"[{method_color}]{request.method:6}[/{method_color}] "
            f"[white]{request.url.path}[/white] "
            f"[{status_color}]{response.status_code}[/{status_color}] "
            f"[magenta]{total_processing_time:.3f}s[/magenta]"
        )

        return response
    

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True
    )    

    if os.getenv("ENVIROMENT") == "production":
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["localhost:8000", "127.0.0.1:8000"]
        )