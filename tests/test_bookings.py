import pytest

@pytest.mark.anyio
async def test_booking_success_decrements_inventory(client, seed_data):
    """
    Test successful booking on Flight 1 (LHR->JFK, 5 seats).
    Verify 201 Created, reference format, and inventory update.
    """
    flight_id = seed_data[0].id
    payload = {
        "flight_id": flight_id,
        "passenger_name": "Jane Doe",
        "passport_number": "AB123456",
        "seat_number": "14A"
    }
    
    response = await client.post("/bookings/", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["reference"].startswith("FH-")
    assert data["passenger_name"] == "Jane Doe"
    
    # Verify that available_seats on the flight decremented from 5 to 4
    flight_resp = await client.get(f"/flights/{flight_id}")
    assert flight_resp.json()["available_seats"] == 4


@pytest.mark.anyio
async def test_overbooking_prevention_409_conflict(client, seed_data):
    """
    Test the critical business rule: No overbooking allowed.
    Flight 2 has only 1 seat. First booking should succeed, second should return 409.
    """
    flight_id = seed_data[1].id
    
    # First booking: Success
    payload1 = {
        "flight_id": flight_id,
        "passenger_name": "First Passenger",
        "passport_number": "PASS01",
        "seat_number": "1A"
    }
    resp1 = await client.post("/bookings/", json=payload1)
    assert resp1.status_code == 201
    
    # Second booking on the same flight: Fail with 409 Conflict
    payload2 = {
        "flight_id": flight_id,
        "passenger_name": "Second Passenger",
        "passport_number": "PASS02",
        "seat_number": "1B"
    }
    resp2 = await client.post("/bookings/", json=payload2)
    assert resp2.status_code == 409
    assert resp2.json()["detail"] == "No seats available on this flight"


@pytest.mark.anyio
async def test_cancellation_restores_seat_count(client, seed_data):
    """
    Test that deleting a booking restores the available_seats on the flight.
    """
    flight_id = seed_data[0].id
    payload = {
        "flight_id": flight_id,
        "passenger_name": "John Smith",
        "passport_number": "CD789012",
        "seat_number": "5C"
    }
    
    # 1. Create booking
    create_resp = await client.post("/bookings/", json=payload)
    reference = create_resp.json()["reference"]
    
    # 2. Verify seats decremented (5 -> 4)
    f_resp_before = await client.get(f"/flights/{flight_id}")
    assert f_resp_before.json()["available_seats"] == 4
    
    # 3. Cancel booking
    cancel_resp = await client.delete(f"/bookings/{reference}")
    assert cancel_resp.status_code == 200
    
    # 4. Verify seats restored (4 -> 5)
    f_resp_after = await client.get(f"/flights/{flight_id}")
    assert f_resp_after.json()["available_seats"] == 5


@pytest.mark.anyio
async def test_invalid_seat_number_validation_422(client, seed_data):
    """
    Test that invalid seat numbers (not matching pattern) return 422 Unprocessable Entity.
    """
    flight_id = seed_data[0].id
    payload = {
        "flight_id": flight_id,
        "passenger_name": "Jane Doe",
        "passport_number": "AB12345",
        "seat_number": "ZZ"  # Invalid; regex requires digits followed by A-F
    }
    
    response = await client.post("/bookings/", json=payload)
    assert response.status_code == 422
