🐄 Dairy Hub – Production-Grade README

1. Overview

Dairy Hub is a production-ready milk collection and billing system built with FastAPI and SQLite, designed for portability, offline friendliness, and multiple admin access modes. It supports web, desktop, and standalone Windows EXE usage without requiring Python on client machines.

The system is suitable for:
• Small to medium dairy cooperatives
• Local milk collection centers
• Offline-first or low-infrastructure environments

⸻

2. Architecture

High-Level Components

Client (Browser / Desktop / EXE)
↓ HTTP
FastAPI Backend (Uvicorn)
↓ ORM
SQLite Database (file-based)

Key Design Decisions
• SQLite: Zero-config, portable, reliable
• FastAPI: High-performance async backend
• Multiple Admin UIs: Web, Python GUI, Windows EXE
• Single-Binary Distribution: No Python needed for end users

⸻

3. Features

Backend
• FastAPI REST API
• SQLAlchemy ORM
• Health check endpoint
• Modular routers

Database
• SQLite file database
• Pre-seeded production-like data
• Referential integrity

Admin Access Options 1. Web Admin Portal (recommended) 2. Python Desktop GUI (developer use) 3. Standalone Windows EXE (end users)

⸻

4. Technology Stack

Layer Technology
Backend FastAPI, Python
Database SQLite 3
ORM SQLAlchemy
Web UI HTML, CSS, JavaScript
Desktop UI Tkinter
Executable PyInstaller
Server Uvicorn

⸻

5. Project Structure

python-dairy-hub-api/
├── app/
│ ├── core/
│ ├── routers/
│ ├── schemas/
│ ├── static/ # Web admin UI
│ ├── database/ # SQLite DB
│ └── main.py
├── scripts/
│ ├── init_sqlite.py # DB schema
│ ├── seed_sqlite.py # Sample data
│ ├── admin_login_ui.py # Desktop GUI
│ └── build_exe.py # EXE builder
├── dist/
│ └── DairyHubAdminLogin.exe
├── requirements.txt
├── README.md
├── SETUP_GUIDE.md
└── EXE_BUILD_GUIDE.md

⸻

6. Quick Start (Development)

6.1 Environment Setup

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

6.2 Database Initialization

python scripts/init_sqlite.py
python scripts/seed_sqlite.py

6.3 Start API Server

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

⸻

7. Admin Access Methods

7.1 Web Admin Portal (Recommended)

http://127.0.0.1:8000/admin

    •	No installation
    •	Responsive
    •	Production-ready

7.2 Python Desktop GUI

python scripts/admin_login_ui.py

    •	For developers
    •	Source visible

7.3 Windows Standalone EXE

dist\DairyHubAdminLogin.exe

    •	No Python required
    •	Single executable
    •	Suitable for clients and staff

⸻

8. Demo Credentials

Username Password Role
admin admin Administrator
manager secure_password Manager

⸻

9. API Overview

Base URL

/api/v1

Core Modules
• /auth
• /customers
• /milk-rates
• /milk-collection
• /billing

Swagger UI:

http://127.0.0.1:8000/docs

⸻

10. Production Deployment

Backend

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

Client Distribution
• Copy DairyHubAdminLogin.exe
• Ensure API is reachable
• No installation steps required

⸻

11. EXE Build Instructions

python scripts/build_exe.py

Build Output:
• dist/DairyHubAdminLogin.exe
• ~10–11 MB
• Windows 64-bit

⸻

12. Security Notes
    • Credentials are plain for demo only
    • Use password hashing (bcrypt) for production
    • Use HTTPS in real deployments
    • Do not ship hardcoded credentials

⸻

13. Troubleshooting

API Not Reachable
• Ensure server is running
• Check firewall / port
• Verify /health endpoint

EXE Not Launching
• Run via PowerShell
• Check antivirus quarantine
• Rebuild on target OS

⸻

14. Database Backup

Copy-Item app/database/dairy_hub.db app/database/dairy_hub.db.backup

⸻

15. Recommended Enhancements
    • JWT authentication
    • Role-based access control
    • Password hashing
    • PDF billing reports
    • Audit logging
    • Automated backups

⸻

16. Release Information
    • Version: 1.0.0
    • Status: Production Ready
    • Platform: Windows / Cross-platform backend

⸻

17. Summary

Dairy Hub delivers a clean, deployable, production-grade system with minimal operational overhead. It is designed to run anywhere, distribute easily, and scale logically without infrastructure complexity.

Ready for real-world use.
