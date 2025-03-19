from django.urls import path

from llm import views

urlpatterns = [
    path(
        "",
        view=views.HomePageView.as_view(),
        name="home",
    ),
    path(
        "history/",
        view=views.HistoryPageView.as_view(),
        name="history",
    ),
    path(
        "summary/<uuid:summary_uid>/",
        view=views.SummaryPageView.as_view(),
        name="summary",
    ),
]
