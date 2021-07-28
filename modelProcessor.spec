# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(5000)
block_cipher = None

import PyMCTranslate
import minecraft_model_reader
import amulet
import os
import glob
from typing import Dict, Tuple, Set



AMULET_PATH = amulet.__path__[0]
PYMCT_PATH = os.path.abspath(os.path.dirname(PyMCTranslate.__file__))
REAL_PYMCT_PATH = (
    PYMCT_PATH if not os.path.islink(PYMCT_PATH) else os.readlink(PYMCT_PATH)
)  # I have this linked by a symbolic link
MINECRAFT_MODEL_READER = os.path.abspath(
    os.path.dirname(minecraft_model_reader.__file__)
)


a = Analysis(['modelProcessor.py'],
             pathex=['C:\\Users\\camer\\OneDrive\\Documents\\GitHub\\ModelToMinecraft'],
             binaries=[],
             datas=[],
             hiddenimports=['trimesh','amulet','PyMCTranslate'],
             hookspath=[os.path.join(PyMCTranslate.__path__[0], "__pyinstaller"),],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
			 
			 
			 
added_source: Set[str] = set([v[1] for v in a.pure])
missing_source: Dict[str, Tuple[str, str]] = {}
for module_path in (
    AMULET_PATH,
    PYMCT_PATH,
    MINECRAFT_MODEL_READER,
):
    for path in glob.glob(
        os.path.join(os.path.abspath(module_path), "**", "*.py"), recursive=True
    ):
        if path not in added_source:
            rel_path: str = os.path.relpath(path, os.path.dirname(module_path))
            imp_path = rel_path.replace(os.sep, ".")[:-3]
            if imp_path.endswith(".__init__"):
                imp_path = imp_path[:-9]
            missing_source[path] = (rel_path, imp_path)

if missing_source:
    print("These source files are not included in the build.")
    for path in missing_source:
        print("\t", path)
non_data_ext = ["*.pyc", "*.py", "*.dll", "*.so", "*.dylib"]

a.datas += Tree(AMULET_PATH, "amulet", excludes=non_data_ext)
a.datas += Tree(MINECRAFT_MODEL_READER, "minecraft_model_reader", excludes=non_data_ext)
a.datas += Tree(PYMCT_PATH, "PyMCTranslate", excludes=non_data_ext + ["json"])
a.datas += [
    (
        os.path.join("PyMCTranslate", "build_number"),
        os.path.join(PYMCT_PATH, "build_number"),
        "DATA",
    )
]


print("Added data files")
for d in filter(lambda dt: "PyMCTranslate" in dt[0], a.datas):
    print("\t", d)
sys.stdout.flush()  # fix the log being out of order

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)


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
	      icon="icon.ico",
          console=True )
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Amulet",
)

app = BUNDLE(
    coll,
    name="amulet.app",
    icon="icon.ico",
    bundle_identifier="com.amulet-editor.amulet_map_editor",
)