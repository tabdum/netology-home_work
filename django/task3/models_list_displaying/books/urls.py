from django.urls import path
from .views import BookListView, index, DatePageView
urlpatterns = [
    path('', index, name='index'),
    path('books/', BookListView.as_view(), name='books'),
    path('books/<date>/', DatePageView.as_view(), name='date_page'),
]