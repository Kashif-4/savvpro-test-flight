import sys
import os
from pathlib import Path

# Add the backend directory to sys.path to allow imports of database, main, models, etc.
backend_path = str(Path(__file__).parent.parent / "backend")
if backend_path not in sys.path:
    sys.path.append(backend_path)

import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
from models import Flight

# Use in-memory SQLite for isolated testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Creates a fresh in-memory database and session for each test.
    Drops tables after the test is finished.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
async def client(db_session):
    """
    Overrides the get_db dependency to use the test database session.
    Provides an AsyncClient for making requests to the FastAPI app.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    # Use ASGITransport for modern httpx versions (0.27+)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def seed_data(db_session):
    """
    Seeds the in-memory database with the two flights required by the task.
    Flight 1: LHR -> JFK (5 seats)
    Flight 2: DXB -> SIN (1 seat)
    """
    from datetime import datetime, timedelta

    f1 = Flight(
        origin='LHR',
        destination='JFK',
        departure_time=datetime.now() + timedelta(days=1),
        duration_mins=420,
        price=500.0,
        total_seats=5,
        available_seats=5
    )
    f2 = Flight(
        origin='DXB',
        destination='SIN',
        departure_time=datetime.now() + timedelta(days=2),
        duration_mins=450,
        price=600.0,
        total_seats=1,
        available_seats=1
    )
    db_session.add(f1)
    db_session.add(f2)
    db_session.commit()
    db_session.refresh(f1)
    db_session.refresh(f2)
    return [f1, f2]
