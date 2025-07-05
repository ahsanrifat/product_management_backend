# app/main.py

from fastapi import FastAPI, Response, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import asyncio

from .database import engine, Base, get_db
from .routers import users, products, orders
from .metrics.middleware import PrometheusMiddleware
from .metrics.prometheus_exporter import get_prometheus_metrics
from .metrics.system_collector import collect_system_metrics


# Define an async context manager for application startup and shutdown events.
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events for the FastAPI application.
    - Creates database tables on startup if they don't exist.
    - Starts the system metrics collection background task.
    """
    # Create database tables if they don't exist
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created (or already exist).")

    # Start the background task for system metrics collection
    # We use asyncio.create_task to run it concurrently with the main app
    print("Starting system metrics collector...")
    asyncio.create_task(collect_system_metrics())
    print("System metrics collector started.")

    yield  # Application runs

    # Clean up on shutdown (if any specific shutdown logic is needed)
    print("Application shutting down.")


# Initialize FastAPI application with the lifespan context manager
app = FastAPI(
    title="E-commerce Backend API",
    description="A FastAPI backend for an e-commerce platform with user management, product inventory, order processing, JWT authentication, and Prometheus metrics.",
    version="1.0.0",
    lifespan=lifespan,  # Assign the lifespan context manager
)

# Add Prometheus middleware to collect HTTP request metrics
app.add_middleware(PrometheusMiddleware)

# Include routers for different functionalities
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get("/")
async def root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the E-commerce Backend API!"}


@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    """
    Endpoint to expose Prometheus metrics.
    """
    return get_prometheus_metrics()
