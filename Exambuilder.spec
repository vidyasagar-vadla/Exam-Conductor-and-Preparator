# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import sdl2, glew
block_cipher = None


a = Analysis(
    ['Exambuilder.py'],
    pathex=[],
    binaries=[],
    datas=[('exambuilder.kv','.'),('imagess/*.jpg','./imagess'),('imagess/*.png','./imagess'),('QuestionPapers/JAVA/*','./QuestionPapers/JAVA'),('pdfs/*','./pdfs')],
    hiddenimports=['kivy.config','PIL.Image','shutil','mysql.connector','kivymd.icon_definitions','kivy.lang.builder','kivy.lang.parser','win32timezone','datetime'],
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

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Exambuilder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Exambuilder',
)
