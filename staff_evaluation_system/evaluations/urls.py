from django.urls import path
from . import views

urlpatterns = [
    path("records/", views.evaluation_list, name="evaluation_list"),
    path("new/<str:form_type>/", views.evaluation_create, name="evaluation_create"),
    path("records/<int:pk>/", views.evaluation_detail, name="evaluation_detail"),
    path("records/<int:pk>/edit/", views.evaluation_update, name="evaluation_update"),
    path("export/", views.export_evaluations, name="export_evaluations"),
    path("summary/", views.summary, name="evaluation_summary"),
    path("summary/export/", views.export_summary, name="export_summary"),
    path("administrative/", views.administrative_list, name="administrative_list"),
    path("administrative/new/", views.administrative_create, name="administrative_create"),
    path("administrative/<int:pk>/", views.administrative_detail, name="administrative_detail"),
    path("administrative/<int:pk>/edit/", views.administrative_update, name="administrative_update"),
    path("administrative/export/", views.export_administrative, name="export_administrative"),
    path("staff/", views.staff_list, name="staff_list"),
    path("staff/new/", views.staff_create, name="staff_create"),
    path("staff/import/", views.staff_import, name="staff_import"),
    path("archive/", views.archive_list, name="archive_list"),
    path("archive/new/<str:source_type>/<int:pk>/", views.archive_create, name="archive_create"),
    path("archive/export/", views.export_archive, name="export_archive"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
