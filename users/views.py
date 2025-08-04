from django.contrib.auth.views import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from users.models import CustomUser
from users.froms import RegisterUserForm, UpdateUserForm


class DashboardView(TemplateView):
    template_name = "extraordinary_package/index.html"


class UserSignUpView(CreateView):
    """
        Handles the user signup functionality. After successfully registering, the user is redirected
        to the login page.
    """
    template_name = "users/register.html"
    success_url = reverse_lazy("user-login")
    form_class = RegisterUserForm
    success_message = "Your profile was created successfully"


class UserLoginView(LoginView):
    """
        Handles user login functionality. If login fails, an error message is shown.
    """
    template_name = 'users/login.html'
    redirect_authenticated_user = True


