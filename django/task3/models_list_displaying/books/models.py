# coding=utf-8

from django.db import models
from django.urls import reverse


class Book(models.Model):
    name = models.CharField(verbose_name='Название', max_length=64)
    author = models.CharField(verbose_name='Автор', max_length=64)
    pub_date = models.DateField(verbose_name='Дата публикации', auto_now=True, )

    def get_absolute_url(self):
        return reverse('date_page', kwargs={'date': str(self.pub_date)})

    def __str__(self):
        return self.name + " " + self.author


