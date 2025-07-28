import os
import shutil

# Directories to skip
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', 'venv'}

# Source monitoring script
SOURCE_FILE = '.usage_monitor.py'

def deploy_monitors():
    for root, dirs, files in os.walk('.'):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        target_path = os.path.join(root, SOURCE_FILE)
        if not os.path.exists(target_path):
            shutil.copy(SOURCE_FILE, target_path)
            print(f"Deployed to {target_path}")

if __name__ == "__main__":
    deploy_monitors()