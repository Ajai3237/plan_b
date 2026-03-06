from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .permissions import check_permission

def permission_required(permission_name):
    """Decorator to check user permissions."""
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not check_permission(request, permission_name):
                messages.error(request, 'You do not have permission to perform this action.')
                referrer = request.META.get('HTTP_REFERER')
                return redirect(referrer)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator