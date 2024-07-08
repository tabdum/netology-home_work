from datetime import datetime

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from books.models import Book


def index(request):
    return HttpResponse("Hello, world. You're at the books index.")


class BookListView(ListView):

    template_name = 'books/books_list.html'
    model = Book
    context_object_name = 'books'
    paginate_by = 5


class DatePageView(ListView):

    template_name = 'books/date_page.html'
    slug_url_kwarg = 'date'
    context_object_name = 'date_page'

    def get_queryset(self):
        return Book.objects.filter(pub_date=self.kwargs[self.slug_url_kwarg]).order_by('pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        date_list = [str(book.pub_date) for book in Book.objects.all().order_by('pub_date')]
        page_now_index = date_list.index(self.kwargs[self.slug_url_kwarg])
        try:
            ind = page_now_index - 1
            if ind < 0:
                raise IndexError
            page_prev = Book.objects.filter(pub_date=date_list[ind])
            context.update({
                'page_prev': page_prev[0],
                'prev_url': page_prev[0].get_absolute_url(),
            })
        except IndexError:
            context.update({
                'page_prev': 0,
            })
        try:
            page_next = Book.objects.filter(pub_date=date_list[page_now_index + 1])
            context.update({
                'page_next': page_next[0],
                'next_url': page_next[0].get_absolute_url(),
            })
        except IndexError:
            context.update({
                'page_next': 0,
            })
        return context

    # paginator_class = Paginator(get_queryset(), 5)
