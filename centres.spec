# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for BANKILY Multi-Centres Generator
"""

block_cipher = None

a = Analysis(
    ['interface_multi_centres.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'pandas',
        'pandas.io.formats.excel',
        'pandas.io.excel._openpyxl',
        'pandas.io.excel._xlrd',
        'openpyxl',
        'xlrd',
        'reportlab',
        'reportlab.platypus',
        'reportlab.platypus.doctemplate',
        'reportlab.platypus.paragraph',
        'reportlab.platypus.tables',
        'reportlab.lib.colors',
        'reportlab.lib.pagesizes',
        'reportlab.lib.styles',
        'reportlab.lib.units',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'tkcalendar',
        'tempfile',
        'threading',
        'zipfile',
        'shutil',
        'datetime',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy.testing', 'pandas.tests'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BANKILY_Multi_Centres',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/bankily.ico'
)