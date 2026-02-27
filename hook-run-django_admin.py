# PyInstaller runtime hook to patch Django admin.unregister
# jwt_auth.admin tries to unregister BlacklistedToken before it's registered

import django.contrib.admin.sites as admin_sites

_original_unregister = admin_sites.AdminSite.unregister

def _safe_unregister(self, model_or_iterable):
    try:
        _original_unregister(self, model_or_iterable)
    except admin_sites.NotRegistered:
        pass

admin_sites.AdminSite.unregister = _safe_unregister
