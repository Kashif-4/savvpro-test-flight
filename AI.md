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

