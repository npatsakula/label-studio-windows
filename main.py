"""
Label Studio Windows Launcher
Entry point for PyInstaller executable
"""
import sys
import os


def main():
    """Launch Label Studio server."""
    # Set up environment for frozen executable
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
        os.environ['LABEL_STUDIO_BASE_DIR'] = bundle_dir

    # Set Django settings module before any Django imports
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'label_studio.core.settings.label_studio')

    # Monkey-patch admin.site.unregister to be safe against NotRegistered errors
    # This fixes the issue where jwt_auth.admin tries to unregister BlacklistedToken
    # before rest_framework_simplejwt.token_blacklist.admin registers it
    from django.contrib import admin
    _original_unregister = admin.site.unregister

    def _safe_unregister(model_or_iterable):
        try:
            _original_unregister(model_or_iterable)
        except admin.sites.NotRegistered:
            pass  # Model not registered, ignore

    admin.site.unregister = _safe_unregister

    # Import and run label-studio server
    from label_studio.server import main as ls_main

    # Default arguments if none provided
    if len(sys.argv) == 1:
        sys.argv = [sys.argv[0], 'start']

    sys.exit(ls_main())


if __name__ == "__main__":
    main()
