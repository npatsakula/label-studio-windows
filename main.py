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
        # Running as compiled executable
        bundle_dir = sys._MEIPASS
        os.environ['LABEL_STUDIO_BASE_DIR'] = bundle_dir

    # Pre-import token_blacklist admin to ensure models are registered
    # before jwt_auth.admin tries to unregister them
    try:
        import rest_framework_simplejwt
        import rest_framework_simplejwt.token_blacklist
        # Ensure admin is registered
        from django.contrib import admin
        from rest_framework_simplejwt.token_blacklist import admin as token_blacklist_admin  # noqa
    except ImportError:
        pass

    # Import and run label-studio server
    from label_studio.server import main as ls_main

    # Default arguments if none provided
    if len(sys.argv) == 1:
        sys.argv = [sys.argv[0], 'start']

    sys.exit(ls_main())


if __name__ == "__main__":
    main()
