# models.py — SQLAlchemy ORM models for Flight and Booking

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Flight(Base):
    """
    Represents a scheduled flight with seat inventory.
    available_seats is decremented on booking and restored on cancellation.
    """
    __tablename__ = "flights"

    id              = Column(Integer, primary_key=True, index=True)
    origin          = Column(String(3), nullable=False, index=True)       # IATA code, e.g. "LHR"
    destination     = Column(String(3), nullable=False, index=True)       # IATA code, e.g. "DXB"
    departure_time  = Column(DateTime, nullable=False, index=True)        # UTC naive datetime
    duration_mins   = Column(Integer, nullable=False)                     # flight duration in minutes
    price           = Column(Float, nullable=False)                       # price per seat in USD
    total_seats     = Column(Integer, nullable=False)                     # immutable capacity
    available_seats = Column(Integer, nullable=False)                     # mutable; locked on booking

    # One flight → many bookings
    bookings = relationship("Booking", back_populates="flight")

    def __repr__(self) -> str:
        return (
            f"<Flight id={self.id} {self.origin}->{self.destination} "
            f"dep={self.departure_time} seats={self.available_seats}/{self.total_seats}>"
        )


class Booking(Base):
    """
    Represents a confirmed or cancelled seat reservation on a Flight.
    status is either 'confirmed' or 'cancelled'.
    """
    __tablename__ = "bookings"

    id              = Column(Integer, primary_key=True, index=True)
    reference       = Column(String(8), unique=True, nullable=False, index=True)  # e.g. "FH-A1B2"
    flight_id       = Column(Integer, ForeignKey("flights.id"), nullable=False)
    passenger_name  = Column(String(100), nullable=False)
    passport_number = Column(String(20), nullable=False)
    seat_number     = Column(String(4), nullable=False)                   # e.g. "14A", "3F"
    status          = Column(String(10), nullable=False, default="confirmed")  # confirmed | cancelled

    # Many bookings → one flight
    flight = relationship("Flight", back_populates="bookings")

    def __repr__(self) -> str:
        return (
            f"<Booking ref={self.reference} flight_id={self.flight_id} "
            f"pax='{self.passenger_name}' seat={self.seat_number} status={self.status}>"
        )
