from functools import wraps
from django.shortcuts import redirect
from users.models import Employee
from icecream import ic


def employee_permission(redirect_url='dashboard'):
    """
        Decorator that redirects non-employee users to a specified URL.

        Usage:
            @employee_required_with_redirect(redirect_url='access-denied')
            def my_view(request):
                ...
        """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect('user-sign-in')
            employee = Employee.objects.filter(id=request.user.id)
            if not employee:
                return redirect(redirect_url)

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator

