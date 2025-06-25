# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for BANKILY Multi-Commerçants Generator
"""

block_cipher = None

a = Analysis(
    ['interface_multi_commercants.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
    ],
    hiddenimports=[
        # Core dependencies
        'pandas',
        'pandas.io.formats.excel',
        'pandas.io.excel._base',
        'pandas.io.excel._openpyxl',
        'pandas.io.excel._xlrd',
        'openpyxl',
        'openpyxl.workbook',
        'openpyxl.worksheet',
        'xlrd',
        'xlrd.biffh',
        
        # ReportLab dependencies
        'reportlab',
        'reportlab.platypus',
        'reportlab.platypus.doctemplate',
        'reportlab.platypus.paragraph',
        'reportlab.platypus.tables',
        'reportlab.lib',
        'reportlab.lib.colors',
        'reportlab.lib.pagesizes',
        'reportlab.lib.styles',
        'reportlab.lib.units',
        'reportlab.pdfgen',
        'reportlab.pdfgen.canvas',
        
        # Tkinter and GUI
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'tkcalendar',
        
        # System modules
        'tempfile',
        'threading',
        'zipfile',
        'shutil',
        'datetime',
        'os',
        'sys',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'matplotlib',
        'numpy.testing',
        'pandas.tests',
        'test',
        'unittest',
    ],
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
    name='BANKILY_Multi_Commercants',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX compression for stability
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/bankily.ico'  # Icon if available
)