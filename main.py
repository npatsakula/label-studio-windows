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

    # Import and run label-studio server
    from label_studio.server import main as ls_main

    # Default arguments if none provided
    if len(sys.argv) == 1:
        sys.argv = [sys.argv[0], 'start']

    sys.exit(ls_main())


if __name__ == "__main__":
    main()
