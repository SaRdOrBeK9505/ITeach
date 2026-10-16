from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("", views.StudentListCreateView.as_view(), name="list-create"),
    path("<int:pk>/", views.StudentDetailView.as_view(), name="detail"),
]
