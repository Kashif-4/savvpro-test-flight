from datetime import datetime, timedelta
from database import engine, Base, SessionLocal
from models import Flight


def seed_database():
    """
    Drops all tables, recreates them, and populates the flights table
    with 10 realistic sample flights for May and June 2026.
    """
    print("--- Initializing Database Seed ---")
    
    # 1. Reset Database
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)

    # 2. Prepare Sample Data
    # List of (origin, destination, departure_offset_days, duration, price)
    sample_flights = [
        ("LHR", "DXB", 1, 420, 550.0),   # London to Dubai
        ("JFK", "LHR", 3, 410, 850.0),   # New York to London
        ("DXB", "SIN", 5, 440, 450.0),   # Dubai to Singapore
        ("SIN", "HND", 7, 390, 320.0),   # Singapore to Tokyo
        ("LAX", "JFK", 9, 320, 280.0),   # Los Angeles to New York
        ("CDG", "AMS", 11, 75, 150.0),   # Paris to Amsterdam
        ("IST", "DXB", 13, 270, 210.0),  # Istanbul to Dubai
        ("BKK", "SYD", 15, 540, 720.0),  # Bangkok to Sydney
        ("NBO", "IST", 17, 380, 480.0),  # Nairobi to Istanbul
        ("AMS", "LHR", 19, 70, 180.0),   # Amsterdam to London
    ]

    base_date = datetime(2026, 5, 10, 10, 0, 0)
    
    db = SessionLocal()
    try:
        print("Inserting 10 flights...")
        for origin, dest, days, duration, price in sample_flights:
            departure = base_date + timedelta(days=days)
            flight = Flight(
                origin=origin,
                destination=dest,
                departure_time=departure,
                duration_mins=duration,
                price=price,
                total_seats=150,
                available_seats=150
            )
            db.add(flight)
        
        db.commit()
        print("Seed completed successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
