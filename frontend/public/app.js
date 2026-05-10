document.addEventListener('DOMContentLoaded', () => {
    const API_BASE = '/api';

    const searchForm = document.getElementById('search-form');
    const flightsContainer = document.getElementById('flights-container');
    const flightsError = document.getElementById('flights-error');

    const lookupForm = document.getElementById('lookup-form');
    const bookingsContainer = document.getElementById('bookings-container');
    const lookupError = document.getElementById('lookup-error');

    const bookingModal = document.getElementById('booking-modal');
    const closeModalTop = document.getElementById('close-modal-top');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const bookingForm = document.getElementById('booking-form');
    const bookingError = document.getElementById('booking-error');
    const bookingSuccess = document.getElementById('booking-success');
    const modalFlightSummary = document.getElementById('modal-flight-summary');

    // Load initial flights
    fetchFlights();

    // Flight Search
    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const origin = document.getElementById('origin').value.trim();
        const destination = document.getElementById('destination').value.trim();
        const date = document.getElementById('date').value;

        const params = new URLSearchParams();
        if (origin) params.append('origin', origin);
        if (destination) params.append('destination', destination);
        if (date) params.append('date', date);

        fetchFlights(params);
    });

    async function fetchFlights(params = new URLSearchParams()) {
        try {
            flightsError.style.display = 'none';
            flightsContainer.innerHTML = '<p style="text-align: center; width: 100%; color: var(--text-muted); font-size: 1.2rem;">Loading premium flights...</p>';
            
            const queryString = params.toString();
            const url = `${API_BASE}/flights${queryString ? '?' + queryString : ''}`;
            
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const flights = await response.json();
            renderFlights(flights);
        } catch (error) {
            console.error('Error fetching flights:', error);
            flightsError.textContent = 'Failed to load flights. Please try again later.';
            flightsError.style.display = 'block';
            flightsContainer.innerHTML = '';
        }
    }

    function renderFlights(flights) {
        flightsContainer.innerHTML = '';
        
        if (flights.length === 0) {
            flightsContainer.innerHTML = '<p style="text-align: center; width: 100%; color: var(--text-muted); font-size: 1.2rem;">No flights found matching your criteria. Try adjusting your search.</p>';
            return;
        }

        flights.forEach(flight => {
            const dateObj = new Date(flight.departure_time);
            const dateStr = dateObj.toLocaleDateString(undefined, { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' });
            const timeStr = dateObj.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
            
            const card = document.createElement('div');
            card.className = 'flight-card';
            
            card.innerHTML = `
                <div class="route-header">
                    <span class="iata-code">${flight.origin}</span>
                    <div class="flight-icon-wrapper">
                        <span class="flight-icon">✈️</span>
                        <span class="flight-duration">${Math.floor(flight.duration_mins / 60)}h ${flight.duration_mins % 60}m</span>
                    </div>
                    <span class="iata-code">${flight.destination}</span>
                </div>
                
                <div class="flight-details">
                    <div class="detail-row">
                        <span class="detail-label">Departure</span>
                        <span class="detail-value">${dateStr} &bull; ${timeStr}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Available Seats</span>
                        <span class="detail-value" style="color: ${flight.available_seats < 10 ? '#ef4444' : 'inherit'}">${flight.available_seats} / ${flight.total_seats}</span>
                    </div>
                </div>
                
                <div class="card-footer">
                    <div class="price-box">
                        <span class="price-label">Price</span>
                        <span class="price-value">$${flight.price.toFixed(2)}</span>
                    </div>
                    <button class="primary-btn book-btn" data-flight='${JSON.stringify(flight).replace(/'/g, "&apos;")}' ${flight.available_seats === 0 ? 'disabled' : ''}>
                        ${flight.available_seats === 0 ? 'Sold Out' : 'Book Now'}
                    </button>
                </div>
            `;
            
            flightsContainer.appendChild(card);
        });

        // Add event listeners to book buttons
        document.querySelectorAll('.book-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const flight = JSON.parse(e.target.getAttribute('data-flight'));
                openBookingModal(flight);
            });
        });
    }

    // Modal logic
    function openBookingModal(flight) {
        document.getElementById('modal-flight-id').value = flight.id;
        
        const dateObj = new Date(flight.departure_time);
        modalFlightSummary.innerHTML = `
            <strong>${flight.origin} to ${flight.destination}</strong><br>
            <span style="color: var(--text-muted); font-size: 0.9em;">Departure: ${dateObj.toLocaleString()}</span><br>
            <span style="color: var(--accent); font-weight: bold; font-size: 1.1em;">Price: $${flight.price.toFixed(2)}</span>
        `;
        
        bookingError.style.display = 'none';
        bookingSuccess.style.display = 'none';
        bookingForm.reset();
        
        bookingModal.showModal();
    }

    closeModalTop.addEventListener('click', () => bookingModal.close());
    closeModalBtn.addEventListener('click', () => bookingModal.close());

    // Submit Booking
    bookingForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        bookingError.style.display = 'none';
        bookingSuccess.style.display = 'none';
        
        const payload = {
            flight_id: parseInt(document.getElementById('modal-flight-id').value, 10),
            passenger_name: document.getElementById('passenger_name').value.trim(),
            passport_number: document.getElementById('passport_number').value.trim(),
            seat_number: document.getElementById('seat_number').value.trim().toUpperCase()
        };

        try {
            const response = await fetch(`${API_BASE}/bookings`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok) {
                let errMsg = data.detail || 'Booking failed';
                if (Array.isArray(data.detail)) {
                    errMsg = data.detail.map(d => `${d.loc[d.loc.length - 1]}: ${d.msg}`).join(', ');
                }
                throw new Error(errMsg);
            }

            bookingSuccess.textContent = `Booking successful! Your reference is ${data.reference}`;
            bookingSuccess.style.display = 'block';
            bookingForm.reset();
            
            // Refresh flights to show updated seat count
            fetchFlights();

            // Auto close modal after delay
            setTimeout(() => {
                if (bookingModal.open) bookingModal.close();
            }, 3000);

        } catch (error) {
            bookingError.textContent = error.message;
            bookingError.style.display = 'block';
        }
    });

    // Lookup Booking
    lookupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = document.getElementById('lookup-query').value.trim();
        if (!query) return;

        const isReference = query.toUpperCase().startsWith('FH-');
        const params = new URLSearchParams();
        if (isReference) {
            params.append('reference', query.toUpperCase());
        } else {
            params.append('passenger_name', query);
        }

        try {
            lookupError.style.display = 'none';
            bookingsContainer.innerHTML = '<p style="text-align: center; width: 100%; color: var(--text-muted); font-size: 1.2rem;">Searching for bookings...</p>';

            const response = await fetch(`${API_BASE}/bookings?${params.toString()}`);
            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(errData.detail || 'Failed to fetch bookings');
            }

            const bookings = await response.json();
            renderBookings(bookings);
        } catch (error) {
            lookupError.textContent = error.message;
            lookupError.style.display = 'block';
            bookingsContainer.innerHTML = '';
        }
    });

    function renderBookings(bookings) {
        bookingsContainer.innerHTML = '';
        
        if (bookings.length === 0) {
            bookingsContainer.innerHTML = '<p style="text-align: center; width: 100%; color: var(--text-muted); font-size: 1.2rem;">No bookings found matching your details.</p>';
            return;
        }

        bookings.forEach(booking => {
            const flight = booking.flight;
            const dateObj = new Date(flight.departure_time);
            
            const card = document.createElement('div');
            card.className = 'flight-card'; 
            
            const statusClass = booking.status === 'confirmed' ? 'status-confirmed' : 'status-cancelled';
            
            card.innerHTML = `
                <div class="route-header">
                    <div>
                        <span class="status-badge ${statusClass}">${booking.status}</span>
                        <div style="margin-top: 0.75rem; font-weight: 800; color: var(--secondary); font-size: 1.1rem;">Ref: ${booking.reference}</div>
                    </div>
                    <div style="text-align: right;">
                        <span class="iata-code" style="font-size: 1.8rem; display: flex; align-items: center; gap: 0.5rem;">
                            ${flight.origin} <span style="font-size: 1.2rem; transform: rotate(45deg); color: var(--primary);">✈️</span> ${flight.destination}
                        </span>
                    </div>
                </div>
                
                <div class="flight-details">
                    <div class="detail-row">
                        <span class="detail-label">Passenger</span>
                        <span class="detail-value">${booking.passenger_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Departure</span>
                        <span class="detail-value">${dateObj.toLocaleDateString()} &bull; ${dateObj.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Seat</span>
                        <span class="detail-value" style="font-size: 1.1rem; color: var(--primary);">${booking.seat_number}</span>
                    </div>
                </div>
                
                <div class="card-footer" style="justify-content: flex-end;">
                    ${booking.status === 'confirmed' ? `<button class="primary-btn cancel-btn" data-ref="${booking.reference}">Cancel Booking</button>` : ''}
                </div>
            `;
            
            bookingsContainer.appendChild(card);
        });

        // Add event listeners to cancel buttons
        document.querySelectorAll('.cancel-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                if (!confirm('Are you sure you want to cancel this booking? This action cannot be undone.')) return;
                
                const ref = e.target.getAttribute('data-ref');
                try {
                    const response = await fetch(`${API_BASE}/bookings/${ref}`, {
                        method: 'DELETE'
                    });
                    if (!response.ok) {
                        const err = await response.json();
                        throw new Error(err.detail || 'Failed to cancel booking');
                    }
                    
                    alert(`Booking ${ref} has been cancelled successfully.`);
                    // Refresh lookup
                    document.getElementById('lookup-form').dispatchEvent(new Event('submit', { cancelable: true }));
                    // Refresh flights
                    fetchFlights();
                } catch (err) {
                    alert('Error: ' + err.message);
                }
            });
        });
    }
});
