# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for 領標雷達 (Bidding Radar) Windows Executable

block_cipher = None

a = Analysis(
    ['packaging/gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend/dist', 'frontend', 'static'),
        ('backend', 'backend', 'static'),
    ],
    hiddenimports=[
        'backend.main',
        'backend.routers.tenders',
        'backend.services.pcc_api',
        'backend.models.tender',
        'backend.schemas.tender',
        'backend.database',
        'sqlalchemy',
        'fastapi',
        'uvicorn',
        'httpx',
        'apscheduler',
        'pydantic',
        'pydantic_settings',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='領標雷達',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='領標雷達',
)
