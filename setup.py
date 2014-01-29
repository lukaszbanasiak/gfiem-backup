# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe
from glob import glob

from __init__ import __version__

manifest_template = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<noInheritable/>
<assemblyIdentity
    type="win32"
    name="Microsoft.VC90.CRT"
    version="9.0.21022.8"
    processorArchitecture="x86"
    publicKeyToken="1fc8b3b9a1e18e3b"/>
<file name="MSVCR90.DLL"/>
<file name="MSVCM90.DLL"/>
<file name="MSVCP90.DLL"/>
</assembly>
'''

RT_MANIFEST = 24

properties = {
    'script': 'backup.py',
    'version': __version__,
    'company_name': 'bns',
    'copyright': 'Copyright 2013 Lukasz Banasiak. All rights reserved.',
    'name': 'GFI EventsManager backup',
    'description': 'Wrapper to automated backups in GFI EventsManager',
    'author': 'Lukasz Banasiak',
    'url': 'http://banasiak.me',
    'license': 'GPL',
    'dest_base': 'gfi-backup',
    'other_resources': [
        (RT_MANIFEST, 1, manifest_template % dict(prog='backup'))
    ]
}

setup(
    options={
        'py2exe': {
            'compressed': 1,
            'optimize': 2,
            'bundle_files': 1,
            'dll_excludes': ['w9xpopen.exe']
        }
    },
    console=[properties],
    zipfile=None,  # 'library.zip' if None bundle everything to exe
    data_files=[
        ('', glob('lib\\*.*'))
    ],
)
