# ✈️ FlightHub

## Overview
FlightHub is a modern, full-stack flight search and booking system built as an internal tool for a small travel agency. It provides staff with an intuitive interface to search available flights, book passenger seats with immediate confirmation, and manage existing reservations.
<img width="1897" height="902" alt="image" src="https://github.com/user-attachments/assets/d5bcd305-987c-4bf0-b4c8-feb1c6eb0fdb" />

## Setup Instructions

### Backend Setup
1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Seed the database with sample flight data:
   ```bash
   python seed.py
   ```

### Frontend Setup
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the required Node.js packages:
   ```bash
   npm install
   ```

## Execution

To run the full application, you need to start both the backend and frontend servers in separate terminal windows.

### 1. Run the Backend Server
From the `backend` directory (with your virtual environment activated):
```bash
uvicorn main:app --reload --port 8000
```
*The backend API will be available at http://localhost:8000*

### 2. Run the Frontend Server
From the `frontend` directory:
```bash
npm run dev
```
*The frontend application will be available at http://localhost:3000*

## Assumptions & Design Decisions
- **Internal Tool Environment:** We assumed FlightHub operates as a single-user or small team internal tool, hence there is no complex authentication or multi-tenant setup.
- **CORS Management via Proxy:** To bypass CORS issues and keep the frontend and backend integrated smoothly, the Express frontend server is configured to proxy all `/api` requests to the FastAPI backend.
- **Database:** SQLite is used as the primary database, eliminating the need for a separate database server.
