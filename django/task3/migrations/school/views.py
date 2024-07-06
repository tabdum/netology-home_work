from django.views.generic import ListView
from django.shortcuts import render

from .models import Student


class StudentListView(ListView):
    template_name = 'school/students_list.html'
    model = Student
    ordering = 'group'

    def get_queryset(self):
        return Student.objects.all().prefetch_related('teachers')
