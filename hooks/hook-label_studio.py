"""
PyInstaller analysis-time hook for label_studio.

Triggered when PyInstaller detects `import label_studio`.
Declares all runtime dependencies that PyInstaller can't auto-detect
because Django loads them dynamically (INSTALLED_APPS, middleware, etc.).
"""
import os
from PyInstaller.utils.hooks import (
    collect_all,
    collect_submodules,
    get_package_paths,
)

datas = []
binaries = []
hiddenimports = []

# ── Frontend assets (web/dist/) ──────────────────────────────────────────────
# The React frontend is installed as a separate "web" directory in site-packages,
# NOT inside label_studio. Settings reference it as ../../web/dist/ relative to
# label_studio/core/settings/. We bundle it at "web" so the relative path works.
try:
    _pkg_base, _pkg_dir = get_package_paths('label_studio')
    _web_dir = os.path.join(_pkg_base, 'web')
    if os.path.isdir(_web_dir):
        datas += [(_web_dir, 'web')]
except Exception:
    pass

# ── Packages that need full collection (submodules + data + metadata) ────────
# These have templates, static files, or metadata that must be bundled.
_collect_all_packages = [
    'label_studio',
    'label_studio_sdk',
    'rest_framework',
    'drf_yasg',
    'drf_spectacular',
    'corsheaders',
    'django_extensions',
    'django_filters',
    'django_rq',
    'rules',
    'ldclient',
]

for pkg in _collect_all_packages:
    try:
        _d, _b, _h = collect_all(pkg)
        datas += _d
        binaries += _b
        hiddenimports += _h
    except Exception:
        pass

# ── Django apps loaded dynamically via INSTALLED_APPS ────────────────────────
hiddenimports += [
    # DRF JWT
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.authentication',
    'rest_framework_simplejwt.views',
    'rest_framework_simplejwt.tokens',
    'rest_framework_simplejwt.serializers',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework_simplejwt.token_blacklist.models',
    'rest_framework_simplejwt.token_blacklist.admin',

    # DRF ecosystem
    'drf_generators',
    'drf_dynamic_fields',
    'rest_flex_fields',

    # Django third-party apps
    'django_user_agents',
    'django_user_agents.middleware',
    'annoying',
    'annoying.fields',
    'django_environ',
    'environ',

    # CSP
    'csp',
    'csp.decorators',
    'csp.middleware',
]

# ── Storage backends (loaded conditionally in settings) ──────────────────────
hiddenimports += [
    'storages',
    'storages.backends',
    'storages.backends.s3boto3',
    'storages.backends.gcloud',
    'storages.backends.azure_storage',
    'google.auth',
    'google.auth.transport.requests',
    'google.oauth2',
    'google.cloud.storage',
    'azure.core',
    'azure.core.exceptions',
    'azure.storage.blob',
    'botocore',
    'botocore.exceptions',
    'botocore.handlers',
    'boto3',
]

# ── Feature flags ────────────────────────────────────────────────────────────
hiddenimports += [
    'launchdarkly_server_sdk',
    'box',
    'pyboxen',
]

# ── Task queue ───────────────────────────────────────────────────────────────
hiddenimports += [
    'rq',
    'rq.job',
    'rq.registry',
    'rq.command',
    'redis',
]

# ── Serialization / API schema ───────────────────────────────────────────────
hiddenimports += [
    'coreapi',
    'coreschema',
    'openapi_codec',
    'simplejson',
]

# ── Utilities used at runtime ────────────────────────────────────────────────
hiddenimports += [
    'ranged_fileresponse',
    'pythonjsonlogger',
    'python_json_logger',
    'appdirs',
    'colorama',
    'bleach',
    'defusedxml',
    'xmljson',
    'ijson',
    'ujson',
    'pytz',
    'tldextract',
    'sentry_sdk',
    'pydantic',
    'jsonschema',
    'numpy',
    'pandas',
    'psutil',
    'packaging',
    'packaging.version',
]
