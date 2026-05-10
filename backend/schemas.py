from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class FlightOut(BaseModel):
    """
    Schema for flight details returned to the client.
    Includes current inventory status.
    """
    id: int
    origin: str = Field(..., min_length=2, max_length=3)
    destination: str = Field(..., min_length=2, max_length=3)
    departure_time: datetime
    duration_mins: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    total_seats: int
    available_seats: int

    model_config = ConfigDict(from_attributes=True)


class BookingCreate(BaseModel):
    """
    Schema for creating a new booking.
    Includes strict validation for passenger details and seat format.
    """
    flight_id: int
    passenger_name: str = Field(..., min_length=2)
    passport_number: str = Field(..., min_length=5)
    seat_number: str = Field(..., pattern=r"^\d{1,2}[A-F]$")

    model_config = ConfigDict(from_attributes=True)


class BookingOut(BaseModel):
    """
    Schema for booking confirmation details.
    Nests the FlightOut schema for full context.
    """
    reference: str
    flight: FlightOut
    passenger_name: str
    passport_number: str
    seat_number: str
    status: str

    model_config = ConfigDict(from_attributes=True)
