#!/usr/bin/env python3
"""Generate PyInstaller spec file and run PyInstaller."""
import subprocess, sys, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

# Clean ALL old build artifacts thoroughly
for name in ['bidding-radar.spec', 'build', 'dist', 'backend/build', 'backend/dist']:
    path = os.path.join(ROOT, name)
    if os.path.isdir(path):
        shutil.rmtree(path)
        print(f"Removed directory: {path}")
    elif os.path.isfile(path):
        os.remove(path)
        print(f"Removed file: {path}")

# PyInstaller 6.x uses BUNDLE() instead of removed COLLECT()
SPEC_CONTENT = r"""
# -*- mode: python; coding: utf-8 -*-
from PyInstaller.building.build_main import Analysis, PYZ, EXE
from PyInstaller.building.build_main import BUNDLE  # PyInstaller 6.x replacement for COLLECT
block_cipher = None
a = Analysis(
    ['packaging/gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend/dist', 'frontend'),
        ('backend', 'backend'),
    ],
    hiddenimports=[
        'backend.main', 'backend.routers.tenders',
        'backend.services.pcc_api', 'backend.models.tender',
        'backend.schemas.tender', 'backend.database',
        'sqlalchemy', 'fastapi', 'uvicorn', 'httpx',
        'apscheduler', 'pydantic', 'pydantic_settings',
    ],
    hookspath=[],
    excludes=[],
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True,
          name='領標雷達', debug=False, strip=False, upx=True, console=False)
coll = BUNDLE(exe, a.binaries, a.zipfiles, a.datas,
              strip=False, upx=True, name='領標雷達')
"""

spec_path = os.path.join(ROOT, 'bidding-radar.spec')
with open(spec_path, 'w', encoding='utf-8') as f:
    f.write(SPEC_CONTENT.strip())

print(f"Spec written to {spec_path}")
print(f"Spec first 3 lines:")
for i, line in enumerate(open(spec_path).readlines()[:3]):
    print(f"  {i+1}: {line.rstrip()}")

result = subprocess.run(
    [sys.executable, '-m', 'PyInstaller', '--noconfirm', 'bidding-radar.spec'],
    cwd=ROOT,
)
print(f"PyInstaller exit: {result.returncode}")
sys.exit(result.returncode)
