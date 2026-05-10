import random
import string
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from fastapi import HTTPException
from models import Flight, Booking
import schemas


def get_flights(db: Session, origin: str = None, destination: str = None, date: str = None):
    """
    Fetches flights with optional filtering by origin, destination, and departure date.
    Date filter uses func.date() to compare only the date part of departure_time.
    """
    query = db.query(Flight)
    
    if origin:
        query = query.filter(Flight.origin == origin.upper())
    if destination:
        query = query.filter(Flight.destination == destination.upper())
    if date:
        # date is expected in 'YYYY-MM-DD' format
        query = query.filter(func.date(Flight.departure_time) == date)
        
    return query.all()


def get_flight(db: Session, flight_id: int):
    """
    Fetches a single flight by its ID. Returns None if not found.
    """
    return db.query(Flight).filter(Flight.id == flight_id).first()


def create_booking(db: Session, booking_data: schemas.BookingCreate):
    """
    Implements Task 4/6 Atomic Logic:
    1. Locks the flight row to prevent race conditions.
    2. Checks seat availability.
    3. Generates a unique FH-XXXX reference.
    4. Decrements available seats and saves the booking.
    """
    # Use .with_for_update() to lock the flight row for the duration of the transaction
    flight = db.query(Flight).filter(Flight.id == booking_data.flight_id).with_for_update().first()
    
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    if flight.available_seats <= 0:
        raise HTTPException(status_code=409, detail="No seats available on this flight")

    # Generate unique 8-character reference: FH-XXXX
    while True:
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        reference = f"FH-{suffix}"
        # Check for collision
        exists = db.query(Booking).filter(Booking.reference == reference).first()
        if not exists:
            break

    new_booking = Booking(
        reference=reference,
        flight_id=booking_data.flight_id,
        passenger_name=booking_data.passenger_name,
        passport_number=booking_data.passport_number,
        seat_number=booking_data.seat_number,
        status="confirmed"
    )
    
    # Atomic decrement
    flight.available_seats -= 1
    
    db.add(new_booking)
    try:
        db.commit()
        db.refresh(new_booking)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    return new_booking


def get_bookings(db: Session, passenger_name: str = None, reference: str = None):
    """
    Fetches bookings filtered by passenger name or reference.
    Requires at least one filter to be provided.
    """
    if not passenger_name and not reference:
        return []
        
    query = db.query(Booking)
    
    filters = []
    if passenger_name:
        filters.append(Booking.passenger_name.ilike(f"%{passenger_name}%"))
    if reference:
        filters.append(Booking.reference == reference.upper())
        
    if filters:
        query = query.filter(or_(*filters))
        
    return query.all()


def cancel_booking(db: Session, reference: str):
    """
    Cancels a booking and restores the flight's available seat count.
    Uses row-locking to ensure atomicity.
    """
    # Lock the booking row
    booking = db.query(Booking).filter(Booking.reference == reference.upper()).with_for_update().first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
        
    if booking.status == "cancelled":
        raise HTTPException(status_code=409, detail="Booking is already cancelled")
        
    # Lock the flight row to restore seat
    flight = db.query(Flight).filter(Flight.id == booking.flight_id).with_for_update().first()
    
    booking.status = "cancelled"
    if flight:
        flight.available_seats += 1
        
    try:
        db.commit()
        db.refresh(booking)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    return booking
