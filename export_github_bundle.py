"""
NIRIKSHAN - Automated GitHub Repository Bundler & Deployment Helper
Packages all source code, assets, demo images, presentation slides, and docs for GitHub
"""

import os
import zipfile
import shutil

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_FILENAME = os.path.join(PROJECT_DIR, "NIRIKSHAN_SIH2026_FULL_CODEBASE.zip")

EXCLUDE_DIRS = {"__pycache__", ".git", ".gemini", "env", "venv"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db"}

def create_bundle():
    print("Packaging NIRIKSHAN codebase into a single GitHub-ready ZIP archive...")
    with zipfile.ZipFile(ZIP_FILENAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_DIR):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if file in EXCLUDE_FILES or file.endswith((".zip", ".pyc")):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, PROJECT_DIR)
                zipf.write(full_path, rel_path)
                print(f"  + Added: {rel_path}")

    size_mb = round(os.path.getsize(ZIP_FILENAME) / (1024 * 1024), 2)
    print("==================================================================")
    print(f" SUCCESS: Complete GitHub Codebase Archive Created!")
    print(f" File: {ZIP_FILENAME} ({size_mb} MB)")
    print("==================================================================")

if __name__ == "__main__":
    create_bundle()
