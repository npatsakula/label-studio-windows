# PyInstaller runtime hook for Windows compatibility patches
import sys

# --- Patch 1: Django admin.unregister ---
# jwt_auth.admin tries to unregister BlacklistedToken before it's registered
import django.contrib.admin.sites as admin_sites

_original_unregister = admin_sites.AdminSite.unregister

def _safe_unregister(self, model_or_iterable):
    try:
        _original_unregister(self, model_or_iterable)
    except admin_sites.NotRegistered:
        pass

admin_sites.AdminSite.unregister = _safe_unregister

# --- Patch 2: Windows static file serving ---
# On Windows, after stripping the manifest prefix from an asset path like
# "/react-app/vendor.123.js", the result "/vendor.123.js" is treated as
# drive-root-relative (C:\vendor.123.js), causing safe_join to reject it.
if sys.platform == 'win32':
    import label_studio.core.utils.static_serve as _static_serve
    _original_serve = _static_serve.serve

    def _patched_serve(request, path, document_root=None, show_indexes=False, manifest_asset_prefix=None):
        import posixpath
        from pathlib import Path
        from label_studio.core.utils.manifest_assets import get_manifest_asset
        from django.http import Http404, HttpResponseNotModified
        from django.utils._os import safe_join
        from django.utils.http import http_date
        from django.utils.translation import gettext as _
        from django.views.static import was_modified_since
        from ranged_fileresponse import RangedFileResponse
        import mimetypes

        path = posixpath.normpath(path).lstrip('/')
        fullpath = Path(safe_join(document_root, path))
        if fullpath.is_dir():
            raise Http404(_('Directory indexes are not allowed here.'))
        if manifest_asset_prefix and not fullpath.exists():
            possible_asset = get_manifest_asset(path)
            manifest_asset_prefix = (
                f'/{manifest_asset_prefix}' if not manifest_asset_prefix.startswith('/') else manifest_asset_prefix
            )
            if possible_asset.startswith(manifest_asset_prefix):
                possible_asset = possible_asset[len(manifest_asset_prefix):]
            possible_asset = possible_asset.lstrip('/')  # Fix for Windows
            fullpath = Path(safe_join(document_root, possible_asset))
        if not fullpath.exists():
            raise Http404(_('"%(path)s" does not exist') % {'path': fullpath})
        statobj = fullpath.stat()
        if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'), statobj.st_mtime):
            return HttpResponseNotModified()
        content_type, encoding = mimetypes.guess_type(str(fullpath))
        content_type = content_type or 'application/octet-stream'
        response = RangedFileResponse(request, fullpath.open('rb'), content_type=content_type)
        response['Last-Modified'] = http_date(statobj.st_mtime)
        if encoding:
            response['Content-Encoding'] = encoding
        return response

    _static_serve.serve = _patched_serve
