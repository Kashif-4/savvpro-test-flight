# 📖 FlightHub User Guide

Welcome to FlightHub! This Quick Start guide will show you how to navigate the system, find flights, and manage passenger bookings.

## 🚀 Quick Start

### 1. Search for Flights
When you open FlightHub at `http://localhost:3000`, you will immediately see the **Search Panel**.
- **View All:** By default, all upcoming flights are listed in the table below the search bar.
- **Filter:** Need something specific? Enter an Origin (e.g., `LHR`), Destination, or Date, and click **Search**. The table will instantly update with matching results.

### 2. Book a Flight
Once you find the right flight for your passenger:
1. Click the **Book** button next to the desired flight.
2. A secure booking modal will appear.
3. Fill in the required details:
   - **Passenger Name** (e.g., John Doe)
   - **Passport Number** (minimum 5 characters)
   - **Seat Selection** (e.g., `12A`, `4F`)
4. Click **Confirm Booking**. 
5. You will receive a unique booking reference. **Booking references are unique codes starting with FH- (e.g., `FH-X9Y2`).** Save this code!

### 3. Manage (Cancel) Bookings
If a passenger needs to cancel their flight:
1. Scroll down to the **Manage Bookings** section.
2. Enter the passenger's Name or their unique **FH-XXXX** booking reference.
3. Click **Lookup**. Their booking card will appear.
4. Click **Cancel Booking**. The system will automatically free up their seat on the flight for future passengers.

---
**Tip:** If you try to book a flight with `0` seats available, the system will prevent the booking to ensure no overbooking occurs!
