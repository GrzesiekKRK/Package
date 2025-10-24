from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from users.models import Employee


class EmployeeRequiredMixin(LoginRequiredMixin):
    """
    Mixin for class-based views that requires the user to be an Employee.
    Redirects to `redirect_url` if not.
    """
    redirect_url = 'dashboard'

    def dispatch(self, request, *args, **kwargs):
        if not Employee.objects.filter(id=request.user.id).exists():
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)
