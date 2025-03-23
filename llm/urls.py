from django.urls import path

from llm import views

urlpatterns = [
    path(
        "",
        view=views.HomePageView.as_view(),
        name="home",
    ),
    path(
        "login/",
        view=views.LoginPageView.as_view(),
        name="login",
    ),
    path(
        "signup/",
        view=views.SignupPageView.as_view(),
        name="signup",
    ),
    path(
        "logout/",
        view=views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "summary/",
        view=views.SummaryFormView.as_view(),
        name="summary-form",
    ),
    path(
        "summary/<uuid:uid>/",
        view=views.SummaryPageView.as_view(),
        name="summary",
    ),
]
