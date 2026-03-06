import os
import sys
import subprocess
import shutil

# Configuration
APP_NAME = "AstroCategorizer"
MAIN_SCRIPT = "main.py"
ICON_FILE = "logo.ico"
PNG_LOGO = "logo.png"
VERSION = "1.0.0"

def run_command(command):
    print(f">>> Running: {' '.join(command)}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"!!! Error executing command. Exit code: {result.returncode}")
        sys.exit(result.returncode)

def main():
    print(f"=== {APP_NAME} Windows Build Script ===")
    
    # 1. Check for requirements
    try:
        import PyInstaller
    except ImportError:
        print("!!! PyInstaller not found. Installing...")
        run_command([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 2. Cleanup previous builds
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            print(f"Cleaning {folder}...")
            shutil.rmtree(folder)

    # 3. Run PyInstaller
    print(">>> Building executable with PyInstaller...")
    pyinstaller_cmd = [
        "pyinstaller",
        "--name", f"{APP_NAME}",
        "--windowed",
        "--onedir",
        "--icon", ICON_FILE,
        "--add-data", f"{ICON_FILE};.",
        "--add-data", f"{PNG_LOGO};.",
        "--noconfirm",
        "--clean",
        MAIN_SCRIPT
    ]
    run_command(pyinstaller_cmd)

    # 4. Success check
    exe_path = os.path.join("dist", APP_NAME, f"{APP_NAME}.exe")
    if os.path.exists(exe_path):
        print(f"[OK] Build successful! Executable found at: {exe_path}")
    else:
        print("!!! Build failed: Executable not found.")
        sys.exit(1)

    # 5. Check for Inno Setup (ISCC.exe)
    print(">>> Checking for Inno Setup compiler...")
    iscc_path = shutil.which("iscc")
    if not iscc_path:
        # Common default installation paths
        paths = [
            r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
            r"C:\Program Files\Inno Setup 6\ISCC.exe"
        ]
        for p in paths:
            if os.path.exists(p):
                iscc_path = p
                break

    if iscc_path:
        print(f"Found Inno Setup at: {iscc_path}")
        if not os.path.exists("installer_output"):
            os.makedirs("installer_output")
        print(">>> Compiling Installer...")
        iss_file = f"{APP_NAME}.iss"
        if os.path.exists(iss_file):
            run_command([iscc_path, f"/DMyAppVersion={VERSION}", iss_file])
            print("[OK] Installer created successfully!")
        else:
            print(f"!!! {iss_file} not found. Skipping installer creation.")
    else:
        print("!!! Inno Setup (ISCC.exe) not found in PATH or standard locations.")
        print("Please install Inno Setup 6 to create the installer.")

    print("=== Build Process Finished ===")

if __name__ == "__main__":
    main()
