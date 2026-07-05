#!/usr/bin/env python3
"""
Admin Login UI for Dairy Hub API

A simple tkinter-based GUI for admin login that connects to the FastAPI backend.

Run from repository root:
    python scripts/admin_login_ui.py

Or use the built executable:
    dist/DairyHubAdminLogin.exe

Make sure the FastAPI server is running on http://127.0.0.1:8000
You can modify API_BASE_URL below if the server is on a different machine.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import requests
from threading import Thread
from pathlib import Path
import time
import os

# ============================================================================
# CONFIGURATION - Modify these if needed
# ============================================================================
API_BASE_URL = "http://127.0.0.1:8000"  # Change if API is on different machine
LOGIN_ENDPOINT = f"{API_BASE_URL}/api/v1/auth/login"
# ============================================================================

# Global variable to store the API server process
api_process = None


class AdminLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dairy Hub API - Admin Login")
        self.root.geometry("500x350")
        self.root.resizable(False, False)
        
        # Set window icon (optional)
        self.root.configure(bg="#f0f0f0")
        
        # Center window on screen
        self.center_window()
        
        # Create UI
        self.create_widgets()
        
        # Flag to track login request
        self.is_logging_in = False
        
        # Start API server in background
        self.start_api_server()
    
    def start_api_server(self):
        """Start the FastAPI server in a background thread."""
        server_thread = Thread(target=self._run_api_server, daemon=True)
        server_thread.start()
        
        # Wait for API to be ready
        self.wait_for_api()
    
    def _run_api_server(self):
        """Run the FastAPI server."""
        global api_process
        try:
            # Get the app root directory
            script_dir = Path(__file__).parent
            app_dir = script_dir.parent
            
            # Change to app directory
            os.chdir(app_dir)
            
            # Start uvicorn server
            import uvicorn
            uvicorn.run(
                "app.main:app",
                host="127.0.0.1",
                port=8000,
                log_level="critical",
                access_log=False
            )
        except Exception as e:
            print(f"Error starting API server: {e}")
    
    def wait_for_api(self, max_attempts=30):
        """Wait for API server to be ready."""
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{API_BASE_URL}/docs", timeout=1)
                if response.status_code == 200:
                    print("✓ API server is running")
                    return True
            except Exception:
                pass
            
            time.sleep(0.5)
        
        print("✗ API server failed to start")
        return False
    
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """Create UI elements."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="🐄 Dairy Hub Admin Portal",
            font=("Helvetica", 18, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Milk Collection & Management System",
            font=("Helvetica", 10),
            foreground="#7f8c8d"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Username label and entry
        username_label = ttk.Label(main_frame, text="Username:", font=("Helvetica", 11))
        username_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.username_entry = ttk.Entry(main_frame, width=40, font=("Helvetica", 11))
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        self.username_entry.bind("<Return>", lambda e: self.login_button_click())
        
        # Password label and entry
        password_label = ttk.Label(main_frame, text="Password:", font=("Helvetica", 11))
        password_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.password_entry = ttk.Entry(main_frame, width=40, font=("Helvetica", 11), show="•")
        self.password_entry.pack(fill=tk.X, pady=(0, 20))
        self.password_entry.bind("<Return>", lambda e: self.login_button_click())
        
        # Login button
        self.login_button = ttk.Button(
            main_frame,
            text="Login",
            command=self.login_button_click,
            width=20
        )
        self.login_button.pack(pady=10)
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Status label
        self.status_label = ttk.Label(
            status_frame,
            text="Ready to login",
            font=("Helvetica", 10),
            foreground="#27ae60"
        )
        self.status_label.pack(anchor=tk.W)
        
        # Demo credentials info
        info_frame = ttk.LabelFrame(main_frame, text="Demo Credentials", padding="10")
        info_frame.pack(fill=tk.X, pady=(20, 0))
        
        info_text = ttk.Label(
            info_frame,
            text="Username: admin\nPassword: admin\n\nUsername: manager\nPassword: secure_password",
            font=("Helvetica", 9),
            foreground="#34495e",
            justify=tk.LEFT
        )
        info_text.pack(anchor=tk.W)
    
    def clear_fields(self):
        """Clear input fields."""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.focus()
        self.update_status("Fields cleared", "#27ae60")
    
    def update_status(self, message, color="#27ae60"):
        """Update status label with message and color."""
        self.status_label.config(text=message, foreground=color)
        self.root.update()
    
    def login_button_click(self):
        """Handle login button click."""
        if self.is_logging_in:
            self.update_status("Login already in progress...", "#f39c12")
            return
        
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username:
            messagebox.showwarning("Input Error", "Please enter a username")
            self.username_entry.focus()
            return
        
        if not password:
            messagebox.showwarning("Input Error", "Please enter a password")
            self.password_entry.focus()
            return
        
        # Run login in a separate thread to prevent UI freezing
        login_thread = Thread(target=self.perform_login, args=(username, password))
        login_thread.daemon = True
        login_thread.start()
    
    def perform_login(self, username, password):
        """Perform login request to FastAPI backend."""
        self.is_logging_in = True
        self.login_button.config(state=tk.DISABLED)
        self.update_status("Logging in...", "#3498db")
        
        try:
            # Make login request to FastAPI backend
            response = requests.post(
                LOGIN_ENDPOINT,
                json={"username": username, "password": password},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self.update_status("✓ Login successful!", "#27ae60")
                messagebox.showinfo(
                    "Login Successful",
                    f"Welcome {username}!\n\n{data.get('message', 'You have been logged in successfully.')}"
                )
                self.clear_fields()
            elif response.status_code == 401:
                self.update_status("✗ Invalid credentials", "#e74c3c")
                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password.\n\nPlease try again."
                )
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus()
            else:
                self.update_status(f"✗ Server error ({response.status_code})", "#e74c3c")
                messagebox.showerror(
                    "Login Error",
                    f"Server returned an error:\n{response.status_code} {response.reason}"
                )
        
        except requests.exceptions.ConnectionError:
            self.update_status("✗ Cannot connect to API server", "#e74c3c")
            messagebox.showerror(
                "Connection Error",
                "Could not connect to API server.\n\nThe server should start automatically.\nIf the problem persists, check the console for errors."
            )
        
        except requests.exceptions.Timeout:
            self.update_status("✗ Request timeout", "#e74c3c")
            messagebox.showerror(
                "Timeout Error",
                "The login request timed out.\n\nPlease try again."
            )
        
        except Exception as e:
            self.update_status(f"✗ Error: {str(e)[:30]}", "#e74c3c")
            messagebox.showerror(
                "Error",
                f"An unexpected error occurred:\n{str(e)}"
            )
        
        finally:
            self.is_logging_in = False
            self.login_button.config(state=tk.NORMAL)


def main():
    """Main entry point."""
    print("Starting Dairy Hub Admin Application...")
    print(f"API endpoint: {LOGIN_ENDPOINT}")
    print("\nStarting embedded FastAPI server...\n")
    
    # Initialize database
    try:
        import subprocess
        result = subprocess.run(
            ["python", "scripts/seed_sqlite.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✓ Database initialized")
        else:
            print(f"Warning: Database initialization returned {result.returncode}")
    except Exception as e:
        print(f"Note: Database may already be initialized ({str(e)[:50]})")
    
    root = tk.Tk()
    _ = AdminLoginApp(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nShutting down...")
        root.quit()


if __name__ == "__main__":
    main()
