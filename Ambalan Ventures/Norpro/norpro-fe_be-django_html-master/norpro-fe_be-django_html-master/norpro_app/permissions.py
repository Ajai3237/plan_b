from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
def check_permission(request, path_name):
    """Utility function to check if the user has permission."""
    if not request.user.is_authenticated:
        return False
    
    user = request.user
    if user.is_superuser:
        return True  # Superuser has all permissions

    if user.role:
        return any(perm.path_name == path_name and perm.status == 'Active' for perm in user.role.permissions.all())
    
    return False



