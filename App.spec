# -*- mode: python -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None

a = Analysis(['.\\TinyPID\\App.py'],
	pathex=['.\\TinyPID', '.\\TinyPID\\UI', '.\\TinyPID\\Models', '.\\TinyPID\\Commands'],
	binaries=[],
	datas=[
		('.\\TinyPID\\stylesheets\\*.qss', 'stylesheets'),
		('.\\TinyPID\\translate\\*.qm', 'translate')
	],
	hiddenimports=[],
	hookspath=[],
	runtime_hooks=[],
	excludes=[],
	win_no_prefer_redirects=False,
	win_private_assemblies=False,
	cipher=block_cipher,
	noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
	cipher=block_cipher)

exe = EXE(pyz,
	a.scripts,
	[],
	exclude_binaries=True,
	name='TinyPID',
	debug=True,
	bootloader_ignore_signals=False,
	strip=False,
	upx=True,
	console=True,
	icon='.\\TinyPID\\res\\TinyPID.ico',
	version='version.rc')
coll = COLLECT(exe,
	a.binaries,
	a.zipfiles,
	a.datas,
	strip=False,
	upx=True,
	name='App')