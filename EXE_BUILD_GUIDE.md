# Dairy Hub Admin Login - Standalone Executable (.EXE)

## ✅ Executable Built Successfully!

**Location:** `dist/DairyHubAdminLogin.exe`
**Size:** 10.6 MB
**Platform:** Windows (64-bit)
**No Installation Required!**

---

## 🚀 How to Use

### Prerequisites:
- FastAPI server must be running somewhere (local machine or network)
- Windows 10 or later
- No Python installation needed

### Steps:

1. **Make sure API server is running** (on your development machine or server):
   ```powershell
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   Note: Use `--host 0.0.0.0` if accessing from another machine

2. **Run the executable:**
   - Double-click: `dist/DairyHubAdminLogin.exe`
   - Or from PowerShell: `.\dist\DairyHubAdminLogin.exe`

3. **Login with demo credentials:**
   - **Username:** admin | **Password:** admin
   - **Username:** manager | **Password:** secure_password

4. **Success:** The login GUI will appear!

---

## 🔧 Distribution & Portability

### For Local Use:
```powershell
# Just run the .exe directly
dist\DairyHubAdminLogin.exe
```

### For Remote Deployment:
1. Copy `dist/DairyHubAdminLogin.exe` to any Windows machine
2. Edit the file in a text editor if you need to change API URL (optional, see below)
3. Run the .exe
4. Enter the API server's IP/hostname in the address bar

### To Redistribute:
```powershell
# Create a folder with the exe
mkdir DairyHubAdmin
Copy-Item dist/DairyHubAdminLogin.exe DairyHubAdmin/
Copy-Item SETUP_GUIDE.md DairyHubAdmin/
# Now you can zip and distribute the folder
```

---

## 🔌 Configuring API Server Address

By default, the .exe connects to `http://127.0.0.1:8000` (local machine).

### If API server is on a different machine:

**Option 1: Edit before building (Recommended)**
- Open `scripts/admin_login_ui.py`
- Find line: `API_BASE_URL = "http://127.0.0.1:8000"`
- Change to your server IP/hostname, e.g.:
  ```python
  API_BASE_URL = "http://192.168.1.100:8000"  # Your server IP
  ```
- Rebuild: `python scripts/build_exe.py`

**Option 2: Runtime configuration**
The app will show a connection error if it can't reach the server. The error message will tell you to check the configuration.

---

## 📋 Login Credentials

The executable comes with these demo admin accounts:

| Username | Password | Notes |
|----------|----------|-------|
| admin | admin | Main administrator |
| manager | secure_password | Secondary account |

**To add more users:**
1. Connect to SQLite DB: `app/database/dairy_hub.db`
2. Insert into admin table:
   ```sql
   INSERT INTO admin (username, password) VALUES ('newuser', 'newpass');
   ```
3. Restart API server

---

## 🐛 Troubleshooting

### "Cannot connect to API server"
**Problem:** The .exe can't reach the FastAPI server
**Solutions:**
- Make sure API server is running: `python -m uvicorn app.main:app --reload`
- Check API is accessible at: http://127.0.0.1:8000/health
- If using remote server, update `API_BASE_URL` in `scripts/admin_login_ui.py` and rebuild

### "Invalid username or password"
**Problem:** Login credentials don't work
**Solutions:**
- Double-check username and password (case-sensitive)
- Verify database was seeded: `python scripts/seed_sqlite.py`
- Check admin table: `sqlite3 app/database/dairy_hub.db "SELECT * FROM admin;"`

### Window won't open
**Problem:** .exe clicked but nothing happens
**Solutions:**
- Check Windows Defender didn't block it (allow if prompted)
- Run from PowerShell to see error messages: `.\dist\DairyHubAdminLogin.exe`
- Ensure Python 3.10+ environment was used to build

### "python.dll" or similar errors
**Problem:** Runtime error when launching .exe
**Solutions:**
- Rebuild on the target Windows version/configuration
- Ensure PyInstaller is properly installed: `pip install --upgrade pyinstaller`
- Try running: `python scripts/build_exe.py` again

---

## 🔄 Rebuilding the Executable

If you make changes to the login UI:

```powershell
# 1. Make changes to scripts/admin_login_ui.py
# 2. Rebuild the executable
python scripts/build_exe.py

# 3. New .exe will be at dist/DairyHubAdminLogin.exe
```

The build process will:
- Remove old files
- Recompile with latest changes
- Create a new 10-11 MB .exe

---

## 📦 What's Included in the .EXE

The executable contains:
- ✅ Python runtime (3.13.5)
- ✅ tkinter GUI library
- ✅ requests library (for HTTP calls)
- ✅ All dependencies bundled
- ✅ No external files needed

Total size: ~10.6 MB

---

## 🚨 Important Notes

### Security
- The .exe is NOT obfuscated - Python code can be extracted
- Don't ship with hardcoded credentials
- Use proper authentication for production
- Use HTTPS for remote servers: `https://yourserver.com:443`

### Performance
- First launch may take 2-3 seconds (unpacking)
- Subsequent launches are instant
- Works offline once launched (but needs API connectivity)

### Compatibility
- **Windows Only:** Built for Windows 64-bit
- **Other OS:** Use `python scripts/admin_login_ui.py` instead
- **macOS/Linux:** Build instructions below

---

## 🐧 Building on macOS/Linux

To build on macOS or Linux:

```bash
# Install PyInstaller
pip install pyinstaller

# Build
pyinstaller --onefile --windowed \
  --hidden-import=tkinter \
  --hidden-import=requests \
  scripts/admin_login_ui.py

# Run
./dist/admin_login_ui
```

---

## 📊 Build Information

```
Platform: Windows 10 64-bit
Python Version: 3.13.5
PyInstaller: 6.16.0
Build Date: November 11, 2025
File: dist/DairyHubAdminLogin.exe
Size: 10.6 MB
Type: GUI Application (no console)
```

---

## ✨ Summary

You now have a **standalone Windows executable** that:
- ✅ Works on any Windows machine (no Python needed)
- ✅ Can be copied anywhere and run immediately
- ✅ Connects to your Dairy Hub API
- ✅ Provides professional admin login interface
- ✅ Can be distributed to clients/users

**Get started immediately:**
```powershell
# 1. Make sure API is running
python -m uvicorn app.main:app --reload

# 2. Run the app
dist\DairyHubAdminLogin.exe
```

Happy deploying! 🚀
