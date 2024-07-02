from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug_recept>/', views.calculate, name='calculator'),
]