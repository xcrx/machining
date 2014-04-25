# -*- mode: python -*-
a = Analysis(['__init__.py'],
             pathex=['C:\\Documents and Settings\\Owner\\My Documents\\GitHub\\machining'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\Machining', 'Machining.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='ui\\machining.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'Machining'))
