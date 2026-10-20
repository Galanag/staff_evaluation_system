
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def get_user_role(user):
    if not user.is_authenticated:
        return None

    if user.is_superuser:
        return "ADMIN"

    try:
        return user.profile.role
    except Exception:
        return None


def roles_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped(request, *args, **kwargs):
            role = get_user_role(request.user)

            if role not in allowed_roles:
                raise PermissionDenied(
                    "You do not have permission to access this page."
                )

            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator


def profile_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapped(request, *args, **kwargs):
        if not hasattr(request.user, "profile"):
            messages.error(
                request,
                "Your account has no assigned role. Contact the administrator.",
            )
            return redirect("login")

        return view_func(request, *args, **kwargs)

    return wrapped
