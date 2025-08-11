from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import TemplateView, LoginView
from django.views.generic.edit import DeleteView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from users.models import CustomUser
from users.froms import RegisterUserForm, UpdateUserForm, LoginForm


class DashboardView(TemplateView):
    template_name = "package/pages/landing.html"


class UserSignUpView(CreateView):
    """
        Handles the user signup functionality. After successfully registering, the user is redirected
        to the login page.
    """
    template_name = "users/sign-up.html"
    success_url = reverse_lazy("user-login")
    form_class = RegisterUserForm
    success_message = "Your profile was created successfully"


class UserLoginView(LoginView):
    """
        Handles user login functionality. If login fails, an error message is shown.
    """
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handles the POST request for user login. It validates the login form, authenticates
        the user, and redirects to the products page if successful.

        Args:
            request (HttpRequest): The HTTP request object.
            *args, **kwargs: Additional arguments for the method.

        Returns:
            HttpResponse: The response after processing the login request.
        """
        form = LoginForm(request.POST)

        if form.is_valid():
            username, password = (
                form.cleaned_data["username"],
                form.cleaned_data["password"],
            )

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect("products")

        return render(request, "users/login.html", {"form": form})
