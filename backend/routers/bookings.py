from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/", response_model=schemas.BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    """
    Create a new booking. Returns 201 Created on success.
    Handles atomic inventory check and unique reference generation.
    """
    return crud.create_booking(db, booking_data=booking)


@router.get("/", response_model=List[schemas.BookingOut])
def read_bookings(
    passenger_name: Optional[str] = None,
    reference: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve bookings by passenger name or booking reference.
    At least one filter must be provided; otherwise, returns 400.
    """
    if not passenger_name and not reference:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one search filter (passenger_name or reference) is required"
        )
    return crud.get_bookings(db, passenger_name=passenger_name, reference=reference)


@router.delete("/{reference}")
def cancel_booking(reference: str, db: Session = Depends(get_db)):
    """
    Cancel an existing booking by reference and restore flight inventory.
    Returns 404 if booking is not found or 409 if already cancelled.
    """
    db_booking = crud.cancel_booking(db, reference=reference)
    return {"message": "Booking cancelled successfully", "reference": db_booking.reference}
