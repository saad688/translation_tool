# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Urdu Translation Tool.
Targeting PyQt6.

To build using this spec file:
    pyinstaller UrduTranslator.spec
"""
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Collect PyQt6 components
pyqt6_datas, pyqt6_binaries, pyqt6_hiddenimports = collect_all('PyQt6')

# Collect docx
docx_datas, docx_binaries, docx_hiddenimports = collect_all('docx')

# Collect lxml
lxml_datas, lxml_binaries, lxml_hiddenimports = collect_all('lxml')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=pyqt6_binaries + lxml_binaries,
    datas=pyqt6_datas + docx_datas + lxml_datas,
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'google.genai',
        'google.genai.types',
        'docx',
        'lxml',
    ] + pyqt6_hiddenimports + docx_hiddenimports + lxml_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Using onedir mode
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='UrduTranslator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='UrduTranslator',
)
