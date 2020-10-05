import sys
sys.setrecursionlimit(5000)
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['modelProcessor.py'],
             pathex=['C:\\Users\\camer\\OneDrive\\Documents\\GitHub\\ModelToMinecraft'],
             binaries=[('C:\\Users\\camer\\Anaconda3\\Lib\\site-packages\\trimesh\\*','.dll')],
             datas=[('LevelDB-MCPE-64.dll', '.')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='modelProcessor',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )