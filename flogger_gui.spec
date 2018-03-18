# -*- mode: python -*-

block_cipher = None

added_files = [
	    ( 'flogger_help_icon-1.png', '.' ),
	    ( 'flogger_icon-08.png', '.' ),
	    ( 'flogger_start.png', '.'  ),
	    ( 'flogger_stop.png', '.' ),
	    ( 'flogger_schema-1.0.4.sql', '.'),
         ( 'flogger_about.ui', '.'),              
         ( 'flogger_settings_file.txt', '.'),
         ( 'flogger_resources.qrc', '.'),
         ( 'flogger.sql3.2', '.'),
         ( 'flogger_config_1.ui', '.'),  
         ( 'flogger_help.ui', '.'),  
         ( 'flogger.ui', '.'),
         ( 'flarm_data', '.'),
         ]

added_binaries = [
		( '/usr/lib/x86_64-linux-gnu/libfap.so.5', 'libfap5'),
		( '/usr/lib/libfap.so.6', 'libfap6'),
		]



a = Analysis(['flogger_gui.py'],
             pathex=['/home/pjr/git_neon.2/OGN-Flight-Logger_V3.2'],
             binaries=added_binaries,
#             datas=[],
             datas=added_files ,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='flogger_gui',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='flogger_gui')
