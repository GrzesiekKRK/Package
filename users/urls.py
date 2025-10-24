from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (DashboardView, ClientSignInView, ClientSignUpView, ClientUpdateView,
                         ClientProfileView, ClientDeleteView, EmployeeSignUpView, EmployeeUpdateView)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("login/", ClientSignInView.as_view(), name="user-sign-in"),
    path("logout/", LogoutView.as_view(next_page="user-sign-in"), name="user-logout"),
    path("sign-up/", ClientSignUpView.as_view(), name="user-sign-up"),
    path("update/<slug:slug>/", ClientUpdateView.as_view(), name="user-update-profile"),
    path("profile/<slug:slug>/", ClientProfileView.as_view(), name="user-profile"),
    path("logout/", LogoutView.as_view(next_page="user-sign-in"), name="user-logout"),
    path("delete/<int:pk>/", ClientDeleteView.as_view(), name="user-delete"),
    path("employee/sign-up/", EmployeeSignUpView.as_view(), name="employee-sign-up"),
    path("employee/update/<int:pk>", EmployeeUpdateView.as_view(), name="employee-update-profile"),
    path("tables/", DashboardView.as_view(), name="tables"),
    path("tables/", DashboardView.as_view(), name="billing"),
    path("tables/", DashboardView.as_view(), name='virtual-reality'),
    path("tables/", DashboardView.as_view(), name="rtl"),
    path("tables/", DashboardView.as_view(), name='notifications'),
    path("tables/", DashboardView.as_view(), name='signin'),
    path("tables/", DashboardView.as_view(), name='home'),
    path("tables/", DashboardView.as_view(), name='search'),
    path("tables/", DashboardView.as_view(), name='pricing'),
    path("tables/", DashboardView.as_view(), name='components'),
    path("tables/", DashboardView.as_view(), name='settings'),
    path("tables/", DashboardView.as_view(), name='docs'),
    path("tables/", DashboardView.as_view(), name='demo'),
    path("tables/", DashboardView.as_view(), name='blocks'),

]
