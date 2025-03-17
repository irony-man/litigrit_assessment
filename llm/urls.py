from django.urls import path

from llm import views

urlpatterns = [
    path(
        "",
        view=views.HomePage.as_view(),
        name="home",
    ),
]
