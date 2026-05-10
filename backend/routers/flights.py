from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/flights", tags=["flights"])


@router.get("/", response_model=List[schemas.FlightOut])
def read_flights(
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve flights with optional filtering by origin, destination, and date (YYYY-MM-DD).
    """
    return crud.get_flights(db, origin=origin, destination=destination, date=date)


@router.get("/{flight_id}", response_model=schemas.FlightOut)
def read_flight(flight_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single flight by ID. Returns 404 if the flight does not exist.
    """
    db_flight = crud.get_flight(db, flight_id=flight_id)
    if db_flight is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return db_flight
