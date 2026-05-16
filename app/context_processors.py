from django.conf import settings


def site_context(request):
    """Expose global site settings to all templates."""
    return {
        "site_url": getattr(settings, "SITE_URL", ""),
    }
