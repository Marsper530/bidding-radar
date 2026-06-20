#!/usr/bin/env python3
"""Generate PyInstaller spec file and run PyInstaller."""
import subprocess, sys, os

SPEC = """
# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.building.build_main import Analysis, PYZ, EXE
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
from PyInstaller.building.datastruct import COLLECT
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas,
               strip=False, upx=True, name='領標雷達')
"""

with open('bidding-radar.spec', 'w', encoding='utf-8') as f:
    f.write(SPEC)

print("Spec file written. Running PyInstaller...")
result = subprocess.run(
    [sys.executable, '-m', 'PyInstaller', '--noconfirm', 'bidding-radar.spec'],
    env={**os.environ, 'PYTHONPATH': '.'}
)
sys.exit(result.returncode)
