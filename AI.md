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