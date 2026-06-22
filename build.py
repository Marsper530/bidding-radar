#!/usr/bin/env python3
"""Generate PyInstaller spec file and run PyInstaller."""
import subprocess, sys, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

# Clean ALL old build artifacts
for name in ['bidding-radar.spec', 'build', 'dist', 'backend/build', 'backend/dist']:
    path = os.path.join(ROOT, name)
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)

print("Running PyInstaller directly (onefile mode, no spec needed)...")
result = subprocess.run(
    [
        sys.executable, '-m', 'PyInstaller',
        '--name', '領標雷達',
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
sys.exit(result.returncode)
