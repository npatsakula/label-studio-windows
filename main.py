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

        # Add label_studio directory to sys.path FIRST
        # This is needed because label_studio modules use imports like
        # "from jwt_auth..." instead of "from label_studio.jwt_auth..."
        ls_path = os.path.join(bundle_dir, 'label_studio')
        if ls_path not in sys.path:
            sys.path.insert(0, ls_path)

    # Import and run label-studio server
    from label_studio.server import main as ls_main

    # Default arguments if none provided
    if len(sys.argv) == 1:
        sys.argv = [sys.argv[0], 'start']

    sys.exit(ls_main())


if __name__ == "__main__":
    main()
