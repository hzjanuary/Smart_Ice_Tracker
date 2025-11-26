#!/usr/bin/env python
"""
Smart Ice Tracker - Single Command Entry Point
Run entire system: Camera processor + Streamlit UI
Auto-fetch data from Firebase
"""

import os
import sys
import subprocess
import time
import threading
import signal
from pathlib import Path
from datetime import datetime

# =====================================
# Configuration
# =====================================
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
CAMERA_SCRIPT = SRC_DIR / "core" / "camera_manager.py"
UI_SCRIPT = SRC_DIR / "ui" / "app_camera.py"
STREAMLIT_PORT = 8501

print("=" * 80)
print("🧊 SMART ICE TRACKER - UNIFIED LAUNCHER")
print("=" * 80)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# =====================================
# Check file existence
# =====================================
print("Checking files...")
if not CAMERA_SCRIPT.exists():
    print(f"ERROR: Not found: {CAMERA_SCRIPT}")
    sys.exit(1)
print(f"OK Camera processor: {CAMERA_SCRIPT.name}")

if not UI_SCRIPT.exists():
    print(f"ERROR: Not found: {UI_SCRIPT}")
    sys.exit(1)
print(f"OK Streamlit UI: {UI_SCRIPT.name}\n")

# =====================================
# Global variables to control processes
# =====================================
processes = []
stop_event = threading.Event()

def signal_handler(sig, frame):
    """Handle Ctrl+C"""
    print("\n\nSTOPPING: Received interrupt signal (Ctrl+C)...")
    print("Shutting down all services...\n")
    stop_event.set()
    
    # Kill all processes
    for proc in processes:
        try:
            if proc.poll() is None:  # Process is still running
                proc.terminate()
                print(f"OK Stopped process: {proc.pid}")
        except:
            pass
    
    # Wait max 5 seconds
    for proc in processes:
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    
    print("\n" + "=" * 80)
    print("OK ALL SERVICES STOPPED")
    print("=" * 80)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# =====================================
# 1. Run Camera Processor
# =====================================
def run_camera_processor():
    """Run camera processor in background"""
    print("\n" + "=" * 80)
    print("STARTING: Camera Processor")
    print("=" * 80)
    print("License plate detection + Ice bag counting")
    print("Real-time data logging to Firebase\n")
    
    try:
        # Set environment to suppress warnings
        env = os.environ.copy()
        env['PYTHONWARNINGS'] = 'ignore'
        
        proc = subprocess.Popen(
            [sys.executable, "-W", "ignore", str(CAMERA_SCRIPT)],
            cwd=str(PROJECT_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
            env=env
        )
        processes.append(proc)
        
        # Thread to read output
        def read_output():
            try:
                for line in proc.stdout:
                    # Filter out Streamlit warnings
                    if "ScriptRunContext" not in line and "missing" not in line and "Warning:" not in line:
                        if line.strip():
                            print(f"[CAMERA] {line.rstrip()}")
            except:
                pass
        
        thread = threading.Thread(target=read_output, daemon=True)
        thread.start()
        
        print("OK Camera processor started (PID: {})".format(proc.pid))
        return proc
        
    except Exception as e:
        print(f"ERROR: Failed to start camera: {e}")
        return None

# =====================================
# 2. Run Streamlit UI
# =====================================
def run_streamlit_ui():
    """Run Streamlit UI in background"""
    time.sleep(3)  # Wait for camera processor to start
    
    print("\n" + "=" * 80)
    print("STARTING: Streamlit UI")
    print("=" * 80)
    print("View live camera + Manage Firebase data")
    print("Access: http://localhost:8501\n")
    
    try:
        proc = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", str(UI_SCRIPT), 
             "--logger.level=error",
             "--client.showErrorDetails=false"],
            cwd=str(PROJECT_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        processes.append(proc)
        
        # Thread to read output
        def read_output():
            for line in proc.stdout:
                if line.strip():
                    print(f"[STREAMLIT] {line.rstrip()}")
        
        thread = threading.Thread(target=read_output, daemon=True)
        thread.start()
        
        print("OK Streamlit UI started (PID: {})".format(proc.pid))
        print(f"URL: http://localhost:{STREAMLIT_PORT}\n")
        return proc
        
    except Exception as e:
        print(f"ERROR: Failed to start Streamlit: {e}")
        return None
        
        print("✅ Streamlit UI started (PID: {})".format(proc.pid))
        print(f"🔗 URL: http://localhost:{STREAMLIT_PORT}\n")
        return proc
        
    except Exception as e:
        print(f"❌ Lỗi khởi động Streamlit: {e}")
        return None

# =====================================
# Main - Run both services
# =====================================
def main():
    print("\n" + "=" * 80)
    print("SYSTEM STARTUP")
    print("=" * 80 + "\n")
    
    # Start camera processor
    camera_proc = run_camera_processor()
    if not camera_proc:
        print("ERROR: Failed to start camera processor")
        sys.exit(1)
    
    # Start Streamlit UI
    ui_proc = run_streamlit_ui()
    if not ui_proc:
        print("ERROR: Failed to start Streamlit UI")
        sys.exit(1)
    
    # Access information
    print("\n" + "=" * 80)
    print("SYSTEM RUNNING")
    print("=" * 80)
    print("\nACCESS:")
    print(f"  Streamlit: http://localhost:{STREAMLIT_PORT}")
    print(f"  Camera:    OpenCV window (press 'q' to exit)")
    print(f"\nDATA:")
    print(f"  Ice bags detected: Real-time update -> Firebase")
    print(f"  License plates detected: Real-time update -> Firebase")
    print(f"  Read data from Firebase in Streamlit UI")
    print(f"\nTO STOP:")
    print(f"  Press Ctrl+C in this terminal")
    print(f"  Or press 'q' in the camera window")
    print("\n" + "=" * 80 + "\n")
    
    # Wait until process stops
    try:
        while True:
            time.sleep(1)
            
            # Check process status
            if camera_proc.poll() is not None:
                print("\nWARNING: Camera processor stopped")
                signal_handler(None, None)
            
            if ui_proc.poll() is not None:
                print("\nWARNING: Streamlit UI stopped")
                # Do not stop system, allow camera to run independently
                
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()
