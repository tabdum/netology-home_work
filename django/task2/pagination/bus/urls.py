from django.urls import path
from . import views

urlpatterns = [
    path("", views.BuseStateView.as_view(), name="bus_state"),
]