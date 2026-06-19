#!/usr/bin/env python3
"""
Build script for 領標雷達 Windows executable.
Run this on Windows: python build_exe.py

Requirements (install first):
    pip install -r backend/requirements.txt
    pip install pyinstaller
"""
import subprocess
import sys
import os
import shutil

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))


def run(cmd, **kwargs):
    print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0:
        print(f"FAILED: {' '.join(cmd)}")
        sys.exit(1)


def main():
    print("=" * 60)
    print("領標雷達 - Windows Executable Builder")
    print("=" * 60)

    # 1. Build frontend
    print("\n[1/3] Building frontend...")
    frontend_dir = os.path.join(BACKEND_DIR, 'frontend')
    run(['npm', 'install'], cwd=frontend_dir)
    run(['npm', 'run', 'build'], cwd=frontend_dir)

    # 2. Install Python dependencies
    print("\n[2/3] Installing Python dependencies...")
    run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], cwd=BACKEND_DIR)

    # 3. PyInstaller build
    print("\n[3/3] Building Windows executable with PyInstaller...")
    spec_file = os.path.join(BACKEND_DIR, 'packaging', 'bidding-radar.spec')
    run([sys.executable, '-m', 'PyInstaller', '--noconfirm', spec_file], cwd=BACKEND_DIR)

    # Output
    dist_dir = os.path.join(BACKEND_DIR, 'dist')
    exe_name = '領標雷達'
    exe_dir = os.path.join(dist_dir, exe_name)

    print("\n" + "=" * 60)
    print(f"✅ Build complete!")
    print(f"   Folder: {exe_dir}")
    print(f"   To run: {exe_dir}\\{exe_name}.exe")
    print("=" * 60)


if __name__ == '__main__':
    main()
