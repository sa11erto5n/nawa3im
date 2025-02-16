
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

def is_admin(user):
    " Check if user is admin "
    return user.is_authenticated and user.is_superuser

class AdminOnlyMixin(UserPassesTestMixin):
    """Mixin to allow only superusers (admins) to access the view."""

    def test_func(self):
        """Check if the user is a superuser."""
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def handle_no_permission(self):
        """Handle unauthorized access."""
        raise PermissionDenied("You do not have permission to access this page.")