
from django.urls import path

from . import views

app_name = "evalutions"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path(
        "academic-evaluation/new/",
        views.create_academic_evaluation,
        name="create_academic_evaluation",
    ),
]