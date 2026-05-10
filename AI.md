Task 1 — Project Scaffold
Tool: Gemini 3 Flash

Prompt: Asked AI to generate directory tree, requirements.txt, package.json, and .gitignore stubs based on the MTS.

Output Quality: 5/5 — correct structure generated for a Windows environment.

Corrections: None required; the AI correctly identified that PowerShell commands were needed for file creation.


Task 2 — Database Layer
Tool: Antigravity (Claude Sonnet)

Prompt: Asked AI to implement SQLAlchemy 2.x engine in database.py (SQLite, check_same_thread=False, get_db generator) and two ORM models in models.py (Flight with 8 fields, Booking with 7 fields) from the exact MTS schema spec.

Output Quality: 5/5 — correct SQLAlchemy 2.x session pattern, relationships, and __repr__ generated.

Corrections: None required. Verified with Base.metadata.create_all(engine) → "DB tables created OK" and flighthub.db created on disk.



Task 3 — Pydantic Schemas & Seed Data
Tool: Gemini 3 Flash

Prompt: Directed AI to create Pydantic v2 schemas and a seeding script with 10 flights based on @MTS.md.

Output Quality: 4/5 — Schemas correctly use regex for seat numbers and from_attributes config.

Corrections: I noticed the AI used basic strings for the departure dates in the seed script. I directed it to use Python `datetime` objects for better SQLAlchemy compatibility. I also ensured the seat regex was strictly enforced in `schemas.py` to prevent invalid data entry. also tested seed.py and queried databse and it worked as expected .


Task 4 — CRUD Layer
Tool: Gemini 3 Flash

Prompt: Provided Part 6 atomic pseudocode and requested implementation of 5 CRUD functions with row-level locking.

Output Quality: 5/5 — Implemented all 5 functions with .with_for_update() row locking to prevent race conditions as specified.

Corrections: Initially used relative imports which would fail if the backend is not run as a package. Fixed imports to use absolute-style names consistent with the rest of the backend codebase. I prioritized the use of .with_for_update() for the create_booking function. I verified that the AI implemented a while loop for the reference generator to handle potential ID collisions, ensuring 100% uniqueness for booking references. I also ensured that cancel_booking restores seat counts to the flight table.

Note on Environment: Encountered a persistent IDE pathing issue where the Antigravity/VS Code linter failed to recognize the venv interpreter despite successful terminal execution. I manually configured .vscode/settings.json to point to the virtual environment and confirmed that all pytest and seed operations remained functional in the CLI. This ensured that environment-specific "missing import" ghosts did not stall development progress.


Task 5 — FastAPI Routers
Tool: Gemini 3 Flash (in a new chat)

Prompt: Directed the creation of routers and main.py based on the API contract in @MTS.md.

Output Quality: 5/5

Direction/Correction: I ensured the AI used the lifespan event for database initialization instead of the deprecated @app.on_event pattern. I also verified that the GET /bookings route correctly enforces a requirement for at least one search filter to prevent empty queries.


Task 6 — pytest Test Suite
Tool: Gemini 3 Flash

Prompt: Directed AI to create fixtures using an in-memory SQLite database and implement 7 test cases covering search, booking, overbooking, and cancellation.

Output Quality: 5/5

Corrections/Direction: (copied from terminal )
 .\backend\venv\Scripts\python.exe -m pytest tests/ -v --tb=short
=========================== test session starts ============================
platform win32 -- Python 3.13.5, pytest-9.0.3, pluggy-1.6.0 -- D:\flight\savvpro-test-flight\backend\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\flight\savvpro-test-flight
plugins: anyio-4.13.0
collected 14 items

tests/test_bookings.py::test_booking_success_decrements_inventory[asyncio] PASSED [  7%]
tests/test_bookings.py::test_overbooking_prevention_409_conflict[asyncio] PASSED [ 14%]
tests/test_bookings.py::test_cancellation_restores_seat_count[asyncio] PASSED [ 21%]
tests/test_bookings.py::test_invalid_seat_number_validation_422[asyncio] PASSED [ 28%]
tests/test_bookings.py::test_booking_success_decrements_inventory[trio] PASSED [ 35%]
tests/test_bookings.py::test_overbooking_prevention_409_conflict[trio] PASSED [ 42%]
tests/test_bookings.py::test_cancellation_restores_seat_count[trio] PASSED [ 50%]
tests/test_bookings.py::test_invalid_seat_number_validation_422[trio] PASSED [ 57%]
tests/test_flights.py::test_get_flights_returns_all[asyncio] PASSED   [ 64%]
tests/test_flights.py::test_filter_flights_by_origin[asyncio] PASSED  [ 71%] 
tests/test_flights.py::test_get_flight_by_id_not_found[asyncio] PASSED [ 78%]
tests/test_flights.py::test_get_flights_returns_all[trio] PASSED      [ 85%]
tests/test_flights.py::test_filter_flights_by_origin[trio] PASSED     [ 92%] 
tests/test_flights.py::test_get_flight_by_id_not_found[trio] PASSED   [100%]

============================ 14 passed in 0.35s ============================ 