# 🏛️ FlightHub Architecture

## Tech Stack
- **Backend:** **FastAPI** (Python). Chosen for its high performance, automatic Pydantic validation, out-of-the-box Swagger documentation, and excellent support for asynchronous operations.
- **Frontend:** **Express.js** (Node.js) & **Vanilla JS**. Express was selected to act as a lightweight, fast web server that can seamlessly serve static assets and proxy API requests. Vanilla JS with HTML/CSS was chosen for the client side to keep the application lightweight, dependency-free, and blazing fast.

## Data Model
Our data layer uses SQLAlchemy and consists of two primary entities:

### 1. Flight Entity
Represents an available flight route.
- **Fields:** `id`, `origin`, `destination`, `departure_time`, `duration_mins`, `price`, `total_seats`, `available_seats`.
- **Relationships:** A flight can have multiple bookings (One-to-Many).

### 2. Booking Entity
Represents a confirmed passenger reservation.
- **Fields:** `id`, `reference` (e.g., "FH-1A2B"), `flight_id` (Foreign Key), `passenger_name`, `passport_number`, `seat_number`, `status`.
- **Relationships:** A booking is linked to a single flight.

## The Overbooking Solution
A major challenge in flight booking systems is race conditions—two staff members booking the exact same last seat simultaneously.

To ensure strict data integrity, FlightHub implements **Row-Level Locking** using SQLAlchemy's `.with_for_update()`. 
When a booking request is received:
1. We start a database transaction and query the target flight with a lock (`SELECT ... FOR UPDATE`).
2. We verify `available_seats > 0`.
3. We decrement the seats, generate the booking reference, and commit the transaction.

This guarantees that even under heavy concurrent load, two people clicking "Book" at the exact same millisecond will not result in an overbooked flight.

## Frontend Pattern: Express Proxy
Instead of struggling with complex CORS headers and cross-origin preflight requests, we implemented an Express Proxy pattern.
- The Express server runs on port `3000` and serves the static HTML/CSS/JS.
- It utilizes `http-proxy-middleware` to intercept any requests matching `/api/*`.
- These requests are seamlessly routed to the FastAPI backend on port `8000`, stripping the prefix to match the backend routes.
- **Result:** The frontend code interacts cleanly with `/api/...` as if it were a single unified application.
