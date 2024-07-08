from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from phones.models import Phone


def index(request):
    return redirect('catalog')


class CategoryListView(ListView):
    template_name = 'catalog.html'
    context_object_name = 'phones'
    model = Phone

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_value = self.request.GET.get('sort', 'name')
        col_value = {'min_price': 'price', 'max_price': '-price', 'name': 'name'}
        res = {'sort_res': Phone.objects.all().order_by(col_value[sort_value])}
        context.update(res)
        return context




class PhoneDetailView(DetailView):

    template_name = 'product.html'
    model = Phone
