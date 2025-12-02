import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject


def _get_forced_user():
    """Return (and create if needed) a dev user used to bypass auth in testing.

    Username and email can be controlled by env vars `FORCE_USER` and `FORCE_USER_EMAIL`.
    """
    User = get_user_model()
    username = os.environ.get('FORCE_USER', 'dev_admin')
    email = os.environ.get('FORCE_USER_EMAIL', 'dev_admin@example.com')
    try:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_active': True},
        )
        # Ensure staff and superuser flags so permission checks pass
        changed = False
        if not user.is_staff:
            user.is_staff = True
            changed = True
        if not getattr(user, 'is_superuser', False):
            try:
                user.is_superuser = True
                changed = True
            except Exception:
                # Some custom user models may not have is_superuser; ignore
                pass
        if changed:
            user.save()
        return user
    except Exception:
        # If DB isn't ready or any error occurs, return an AnonymousUser-like object
        class _Anon:
            is_authenticated = True
            is_staff = True
            username = username

        return _Anon()


class ForceAuthMiddleware:
    """
    Middleware to force an authenticated staff user for all requests when
    `settings.AUTH_BYPASS` is True or env var `AUTH_BYPASS` == 'True'.

    This is intended strictly for local testing. Do NOT enable in production.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.enabled = getattr(settings, 'AUTH_BYPASS', os.environ.get('AUTH_BYPASS') == 'True')

    def __call__(self, request):
        if self.enabled:
            # Attach a SimpleLazyObject so DB ops are deferred until accessed
            request.user = SimpleLazyObject(_get_forced_user)
        return self.get_response(request)
