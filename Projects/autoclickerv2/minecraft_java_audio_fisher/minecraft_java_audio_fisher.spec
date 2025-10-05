# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\Julius\\Repos\\Python\\Projects\\autoclickerv2\\minecraft_java_audio_fisher.py'],
    pathex=[],
    binaries=[],
    datas=[('audio_files\\minecraft_fishing_catch_sound_short.wav', 'audio_files')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='minecraft_java_audio_fisher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
