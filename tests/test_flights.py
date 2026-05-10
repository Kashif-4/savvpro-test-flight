import pytest

@pytest.mark.anyio
async def test_get_flights_returns_all(client, seed_data):
    """Verify that GET /flights returns the 2 seeded flights."""
    response = await client.get("/flights/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.anyio
async def test_filter_flights_by_origin(client, seed_data):
    """Verify that filtering by origin=LHR returns exactly 1 flight."""
    response = await client.get("/flights/?origin=LHR")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["origin"] == "LHR"
    assert data[0]["destination"] == "JFK"


@pytest.mark.anyio
async def test_get_flight_by_id_not_found(client, seed_data):
    """Verify that GET /flights/999 returns a 404 error."""
    response = await client.get("/flights/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Flight not found"
