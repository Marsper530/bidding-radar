#!/usr/bin/env python3
"""Build 領標雷達 Windows executable with PyInstaller."""
import subprocess, sys, os, shutil, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

# Clean old build artifacts
for name in ['bidding-radar.spec', 'build', 'dist', 'backend/build', 'backend/dist']:
    path = os.path.join(ROOT, name)
    if os.path.isdir(path):
        shutil.rmtree(path)
        print(f"Removed: {path}")
    elif os.path.isfile(path):
        os.remove(path)
        print(f"Removed: {path}")

print("Running PyInstaller (onefile mode)...")
result = subprocess.run(
    [
        sys.executable, '-m', 'PyInstaller',
        '--name', 'BiddingRadar',
        '--add-data', 'frontend/dist;frontend',
        '--add-data', 'backend;backend',
        '--hidden-import', 'backend.main',
        '--hidden-import', 'backend.routers.tenders',
        '--hidden-import', 'backend.services.pcc_api',
        '--hidden-import', 'backend.models.tender',
        '--hidden-import', 'backend.schemas.tender',
        '--hidden-import', 'backend.database',
        '--hidden-import', 'sqlalchemy',
        '--hidden-import', 'fastapi',
        '--hidden-import', 'uvicorn',
        '--hidden-import', 'httpx',
        '--hidden-import', 'apscheduler',
        '--hidden-import', 'pydantic',
        '--hidden-import', 'pydantic_settings',
        '--onefile',
        '--console',
        '--clean',
        'packaging/gui.py',
    ],
    cwd=ROOT,
)
print(f"PyInstaller exit: {result.returncode}")

# Find the built exe
dist_path = os.path.join(ROOT, 'backend', 'dist')
exe_found = glob.glob(os.path.join(dist_path, 'BiddingRadar.exe'))
if exe_found:
    print(f"EXE found: {exe_found[0]}")
    print(f"Size: {os.path.getsize(exe_found[0]) / 1024 / 1024:.1f} MB")
else:
    print("WARNING: EXE not found in backend/dist/")
    # List all files in backend/dist
    if os.path.isdir(dist_path):
        for f in os.listdir(dist_path):
            print(f"  Found: {f}")

sys.exit(result.returncode)
