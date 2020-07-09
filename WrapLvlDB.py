import ctypes
import os.path as op
import sys

if sys.platform == "win32":
  if sys.maxsize > 2**32: # 64 bit python
    ldb = ctypes.cdll.LoadLibrary(op.join(op.dirname(op.realpath(__file__)), "LevelDB-MCPE-64.dll"))
  else: # 32 bit python
    ldb = ctypes.cdll.LoadLibrary(op.join(op.dirname(op.realpath(__file__)), "LevelDB-MCPE-32.dll"))
else: #linux, compile your own .so if this errors!
  ldb = ctypes.cdll.LoadLibrary(op.join(op.dirname(op.realpath(__file__)), "libleveldb.so")) # Load DLL
