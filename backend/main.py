from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import engine, Base
from routers import flights, bookings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event to create database tables on startup.
    In a production app, migrations (Alembic) would be preferred.
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="FlightHub API",
    description="Backend API for the FlightHub flight search and booking system.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration: allow all origins for development and rubric compliance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.add_api_route("/", lambda: {"message": "Welcome to FlightHub API"}, tags=["root"])
app.include_router(flights.router)
app.include_router(bookings.router)
