from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardSummaryView.as_view(), name="summary"),
    path("analytics/", views.DashboardAnalyticsView.as_view(), name="analytics"),
]
