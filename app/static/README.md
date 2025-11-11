# Dairy Hub Admin Login - UI Options

This directory contains two UI options for admin login to the Dairy Hub API:

## Option 1: Web-based UI (Recommended)

**Access via browser after starting the API:**
- Open: http://127.0.0.1:8000/admin
- Modern, responsive design
- Works on desktop and mobile
- Real-time API connection status
- Beautiful gradient design

### How to use:
1. Start the FastAPI server:
   ```powershell
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Open browser to: http://127.0.0.1:8000/admin

3. Use demo credentials:
   - **Username:** admin | **Password:** admin
   - **Username:** manager | **Password:** secure_password

---

## Option 2: Python Desktop GUI (Alternative)

**Standalone tkinter-based application**
- No browser required
- Native desktop experience
- Lightweight
- Works offline (once launched)

### How to use:

1. Make sure the FastAPI server is running:
   ```powershell
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. In another terminal/PowerShell, run:
   ```powershell
   python scripts/admin_login_ui.py
   ```

3. A window will appear with login form
4. Enter credentials and click Login

### Features:
- ✅ Thread-safe login (non-blocking UI)
- ✅ Connection error handling
- ✅ Clear visual feedback
- ✅ Demo credentials displayed
- ✅ Status messages
- ✅ Keyboard shortcuts (Enter to login)

---

## Demo Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin | Administrator |
| manager | secure_password | Manager |

---

## Troubleshooting

**"Cannot connect to API server"**
- Make sure FastAPI server is running
- Run: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Check that port 8000 is available

**GUI window not appearing**
- Make sure Python tkinter is installed (included by default)
- On Linux: `sudo apt-get install python3-tk`

**Invalid credentials error**
- Verify username and password are correct
- Check database was seeded: `python scripts/seed_sqlite.py`

---

## Quick Start Guide

### Complete Setup (from repository root):

```powershell
# 1. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize and seed database
python scripts/init_sqlite.py
python scripts/seed_sqlite.py

# 4. Start API server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. In another terminal, use either:
# Option A: Web UI (browser)
# Open http://127.0.0.1:8000/admin

# Option B: Desktop GUI
# python scripts/admin_login_ui.py
```

---

## Technical Details

### Web UI (index.html)
- Pure HTML/CSS/JavaScript (no dependencies)
- CORS-enabled for API communication
- Responsive design (mobile-friendly)
- Gradient background with emoji styling
- Real-time connection status indicator

### Python GUI (admin_login_ui.py)
- tkinter (built-in Python library)
- Uses `requests` library for HTTP calls
- Multi-threaded to prevent UI freezing
- Error handling and status updates
- Clipboard-friendly password input masking

---

## API Endpoint

**POST** `/api/v1/auth/login`

Request:
```json
{
  "username": "admin",
  "password": "admin"
}
```

Response (Success - 200):
```json
{
  "status": "success",
  "message": "Login successful"
}
```

Response (Error - 401):
```json
{
  "detail": "Invalid username or password"
}
```
