# 🤖 AI Usage & Direction Log: FlightHub

This document provides a detailed account of the collaborative development process for the FlightHub project. It demonstrates a **Human-in-the-Loop** approach, where I acted as the lead architect and technical reviewer, while AI agents handled the implementation of the specified requirements.

---

## 🏛️ Phase 0: The Architectural "Ground Truth"
To ensure the project met the highest standards for data integrity and professional UI, I used **Claude 4.6 Sonnet (Antigravity)** to establish the Master Technical Specification (MTS) and a granular execution roadmap.

### The Planning Prompt (Claude 4.6 Sonnet)
> **Role:** You are a Principal Technical Architect and Senior Full-Stack Engineer.
> **Objective:** Create a Master Technical Specification (MTS) and a Granular Execution Roadmap for the "FlightHub" project in `TASK.md` considering the rules in `README.md`. Your goal is to ensure the final product scores 100/100 on the assessment rubric by addressing Architecture, Code Quality, Testing, and AI Governance.
> 
> **Architectural Ground Truths:**
> 1. **Data Integrity:** Use SQLAlchemy with SQLite. Implement a Strict Atomic Inventory Check for bookings via database transactions. (Reasoning: Avoid race conditions and overbooking by checking available_seats > 0 within a database transaction).
> 2. **API Excellence:** Follow RESTful conventions. Use Pydantic for all request/response schemas to ensure 100% validation coverage.
> 3. **UI Strategy:** Build a "Search-First" Single Page Application (SPA) feel using a Node/Express backend serving a frontend styled with Pico.css for a professional, lightweight, "No-JS-Framework" look.
> 4. **Testing:** Target 100% pass rate on business rules using pytest and httpx.

---

## 📊 Summary of AI Engagement

| Task | AI Tool | Core Responsibility | Quality Score |
| :--- | :--- | :--- | :--- |
| **0. Planning** | Claude 4.6 Sonnet | Architecture & Roadmap Generation | 5/5 |
| **1. Scaffold** | Gemini 3 Flash | Directory structure & stubs | 5/5 |
| **2. Database** | Claude 4.6 Sonnet | SQLAlchemy models & Engine | 5/5 |
| **3. Schemas** | Gemini 3 Flash | Pydantic v2 & Seed logic | 4/5 |
| **4. CRUD** | Gemini 3 Flash | Atomic logic & Row-locking | 5/5 |
| **5. API** | Gemini 3 Flash | FastAPI Routers & Lifespan | 5/5 |
| **6. Testing** | Gemini 3 Flash | `pytest` suite (14 cases) | 5/5 |
| **7. Proxy** | Gemini 3 Flash | Express Server & API Proxy | 5/5 |
| **8. UI/UX** | Gemini 3.1 Pro | Premium UI/UX Design | 5/5 |

---

## 🛠️ Detailed Task Log & Corrections

### Task 1 — Project Scaffold
* **Tool:** Gemini 3 Flash
* **Prompt:** Asked AI to generate directory tree, `requirements.txt`, `package.json`, and `.gitignore` stubs based on the MTS.
* **Outcome:** Correct structure generated for a Windows environment.
* **Correction:** None required; the AI correctly identified that PowerShell commands were needed for file creation.

### Task 2 — Database Layer
* **Tool:** Antigravity (Claude Sonnet)
* **Prompt:** Implement SQLAlchemy 2.x engine in `database.py` and models in `models.py` from the MTS schema spec.
* **Verification:** Verified with `Base.metadata.create_all(engine)`. Database tables and `flighthub.db` successfully initialized.

### Task 3 — Pydantic Schemas & Seed Data
* **Tool:** Gemini 3 Flash
* **Correction:** I noticed the AI used basic strings for departure dates. I **intervened** and directed it to use Python `datetime` objects for better SQLAlchemy compatibility. I also strictly enforced the seat regex in `schemas.py`.

### Task 4 — CRUD Layer (Atomicity)
* **Tool:** Gemini 3 Flash
* **Direction:** I prioritized the use of `.with_for_update()` for the `create_booking` function to prevent race conditions. I also verified the implementation of a `while` loop for unique reference generation.
* **Correction:** Manually fixed relative imports to absolute imports (`backend.models`) to ensure modularity.

### Task 5 — FastAPI Routers
* **Tool:** Gemini 3 Flash
* **Correction:** Directed the AI to use the **FastAPI Lifespan** event for DB initialization instead of deprecated methods. Added validation to `GET /bookings` to prevent empty search queries.

### Task 6 — pytest Test Suite
* **Tool:** Gemini 3 Flash
* **Outcome:** 14/14 test cases passed.
* **Verification:** Manually executed `.\backend\venv\Scripts\python.exe -m pytest tests/ -v --tb=short` to confirm all business rules (Overbooking, Inventory) were valid.

### Task 7 — Express Proxy Server
* **Tool:** Gemini 3 Flash
* **Direction:** Directed the creation of an Express proxy using `http-proxy-middleware` to forward `/api` requests to port 8000, eliminating CORS issues.

### Task 8 — Premium UI/UX (The Visual Finish)
I switched to **Gemini 3.1 Pro** to ensure a high-quality aesthetic that avoided "generic AI" layouts.

#### The UI Design Prompt (Gemini 3.1 Pro)
> **Role:** Senior Frontend Engineer & UI/UX Designer.
> **Objective:** Implement Task 8 (Frontend UI) for FlightHub. I want this to look like a premium, modern travel startup—not a generic template.
> 
> **Visual Requirements:**
> - **Typography:** Import the 'Inter' or 'Poppins' font from Google Fonts.
> - **Color Palette:** Clean white background with a "Midnight Blue" and "Soft Indigo" theme (#f8fafc body, #ffffff cards).
> - **Search Hero:** Prominent centered search bar with soft shadows and rounded corners (12px).
> - **Results:** Use a **Card-Based** layout instead of a table. Price in bold accent color, sleek "Book Now" buttons.
> - **Constraint:** Use Pico.css for the base, but custom CSS in `style.css` for the premium finish.

* **Correction:** The AI missed the light-theme lock for Pico v2. I manually added `data-theme="light"` to the `<html>` tag to maintain design consistency.

---

## 🔍 Technical Impediments
* **IDE Linter Issue:** VS Code failed to recognize the `venv` path. I resolved this by manually configuring `.vscode/settings.json` and verifying all code via the terminal CLI.
* **Package Imports:** Refined several AI-suggested package paths to ensure standard Python module behavior.

---

## 🎓 Final Reflection
By leveraging **Claude 4.6 Sonnet** for the high-level architecture and **Gemini 3.1 Pro** for the user interface, I was able to deliver a robust, thread-safe system with a modern user experience. My active direction ensured that the AI remained a tool for efficiency, while I maintained control over the business logic and project integrity.