from django import template
from norpro_app.permissions import check_permission


register = template.Library()

@register.simple_tag(takes_context=True)
def has_permission(context, path_name):
    """
    Custom template tag to check if the user has a specified permission.
    Usage: {% has_permission "View User List" as user_permission %}
    """
    request = context['request']
    return check_permission(request, path_name)