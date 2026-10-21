from django.contrib import admin
from django.urls import include, path
from evaluations import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("accounts/login/", views.SignInView.as_view(), name="login"),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/logout/", views.signout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("evaluations/", include("evaluations.urls")),
]
