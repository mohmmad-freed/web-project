# decorators.py

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def student_required(function=None):
    """
    Decorator for views that checks that the user is a student,
    redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and not u.is_superuser,
        login_url='login',
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def admin_required(function=None):
    """
    Decorator for views that checks that the user is an admin,
    raising a PermissionDenied exception if necessary.
    """
    def check_admin(user):
        if user.is_authenticated and user.is_superuser:
            return True
        raise PermissionDenied

    actual_decorator = user_passes_test(
        check_admin
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
