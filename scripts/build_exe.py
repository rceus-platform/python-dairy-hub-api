#!/usr/bin/env python3
"""
Build script to create standalone .exe for Dairy Hub Admin Login UI

Run from repository root:
    python scripts/build_exe.py

This will create:
- dist/DairyHubAdminLogin.exe (standalone executable)
- build/ (temporary build files)
"""

import subprocess
import sys
from pathlib import Path

def build_exe():
    """Build the executable using PyInstaller."""
    
    root = Path(__file__).resolve().parent.parent
    script = root / "scripts" / "admin_login_ui.py"
    
    print("=" * 60)
    print("Dairy Hub Admin Login - Building EXE")
    print("=" * 60)
    
    if not script.exists():
        print(f"Error: {script} not found!")
        sys.exit(1)
    
    print(f"\nBuilding executable from: {script}")
    print("\nThis may take a minute...")
    
    # PyInstaller command with options
    cmd = [
        sys.executable,
        "-m", "PyInstaller",  # Case sensitive on some systems
        "--name=DairyHubAdminLogin",
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--icon=NONE",  # No icon (you can add later)
        "--hidden-import=tkinter",
        "--hidden-import=requests",
        "--clean",  # Clean before build
        str(script)
    ]
    
    try:
        result = subprocess.run(cmd, cwd=root, capture_output=False)
        
        if result.returncode == 0:
            exe_path = root / "dist" / "DairyHubAdminLogin.exe"
            
            print("\n" + "=" * 60)
            print("[OK] Build Successful!")
            print("=" * 60)
            print(f"\nExecutable created at:")
            print(f"   {exe_path}")
            print(f"\nFile size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
            print(f"\n[NEXT] To use:")
            print(f"   1. Make sure FastAPI server is running:")
            print(f"      python -m uvicorn app.main:app --reload")
            print(f"   2. Run the executable:")
            print(f"      dist/DairyHubAdminLogin.exe")
            print(f"\n[INFO] Tips:")
            print(f"   - You can copy the .exe to any Windows machine")
            print(f"   - No Python installation needed on target machine")
            print(f"   - Make sure the API server is accessible from that machine")
            print(f"   - Change API_BASE_URL in admin_login_ui.py if server is remote")
            print("\n" + "=" * 60)
        else:
            print(f"\nError: Build failed with return code: {result.returncode}")
            sys.exit(1)
    
    except Exception as e:
        print(f"\nError during build: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_exe()
