from django.shortcuts import render
from django.views.generic import ListView

import csv
import os

from .utils import DataMixin


def csv_list(path):
    with open(path, encoding='utf-8') as file:
        rows = csv.DictReader(file)
        return list(rows)


class BuseStateView(DataMixin, ListView):
    template_name = 'bus/index.html'
    context_object_name = 'buses'
    allow_empty = False

    def get_queryset(self):
        path = '/home/azamat/PycharmProjects/recepis_proj/pagination/bus/data/bus_s.csv'
        return csv_list(path)
