# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Label Studio
"""

import sys
from pathlib import Path

# Get site-packages path
site_packages = None
for p in sys.path:
    if 'site-packages' in p:
        site_packages = Path(p)
        break

if not site_packages:
    raise RuntimeError("Could not find site-packages directory")

block_cipher = None

# Collect all label_studio data files
datas = [
    (str(site_packages / 'label_studio'), 'label_studio'),
]

# Collect Django and other framework files that might have data
hidden_imports = [
    'label_studio',
    'label_studio.server',
    'label_studio.core',
    'label_studio.core.settings',
    'label_studio.core.urls',
    'label_studio.core.wsgi',
    'django',
    'django.contrib',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.core',
    'django.core.wsgi',
    'django.db',
    'django.db.backends',
    'django.db.backends.sqlite3',
    'django.template',
    'django.template.loaders',
    'django.utils',
    'rest_framework',
    'rest_framework.renderers',
    'corsheaders',
    'drf_yasg',
    'colorlog',
    'xmltodict',
    'ujson',
    'orjson',
    'pillow',
    'PIL',
    'numpy',
    'lxml',
    'defusedxml',
    'htmlmin',
    'bleach',
    'markdown',
    'requests',
    'urllib3',
    'certifi',
    'charset_normalizer',
    'idna',
    'oauthlib',
    'requests_oauthlib',
    'jwt',
    'PyJWT',
    'cryptography',
    'ruamel.yaml',
    'prometheus_client',
    'psutil',
    'lockfile',
    'python_dateutil',
    'pytz',
    'tzdata',
    'six',
    'typing_extensions',
    'packaging',
    'setuptools',
    'wheel',
    'distutils',
    'distutils.version',
    'sqlparse',
    'asgiref',
    'greenlet',
    'gevent',
    'gevent.ssl',
    'gevent.socket',
    'gunicorn',
    'gunicorn.app',
    'gunicorn.app.wsgiapp',
    'gunicorn.arbiter',
    'gunicorn.http',
    'gunicorn.http.wsgi',
    'gunicorn.workers',
    'gunicorn.workers.sync',
    'gunicorn.workers.ggevent',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='label-studio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep console for server output
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
