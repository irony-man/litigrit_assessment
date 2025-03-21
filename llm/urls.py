from django.urls import path

from llm import views

urlpatterns = [
    path(
        "",
        view=views.HomePageView.as_view(),
        name="home",
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
