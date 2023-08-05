# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['run.py'],
             pathex=['/home/amagee/commandfrog/commandfrog'],
             binaries=[],
             datas=[],
             hiddenimports=['commandfrog.operations.pyenv', 'commandfrog.operations.__init__', 'commandfrog.operations.docker', 'commandfrog.operations.files', 'commandfrog.operations.platform', 'commandfrog.operations.shell', 'commandfrog.operations.ssh', 'commandfrog.operations.git', 'commandfrog.operations.nvm', 'commandfrog.operations.apt', 'commandfrog.operations.ubuntu', 'commandfrog.operations.mongo', 'commandfrog.operations.pacman'],
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
          name='run',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
