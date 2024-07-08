from django.db import models
from django.urls import reverse


class Phone(models.Model):
    name = models.CharField(max_length=120, blank=True, null=False, verbose_name='Имя')
    price = models.IntegerField(blank=True, null=False, verbose_name='Цена')
    image = models.URLField(blank=True, null=False, verbose_name='Фото')
    release_date = models.DateField(blank=True, null=False, verbose_name='Дата релиза')
    lte_exists = models.BooleanField(default=False, verbose_name='В наличии')
    slug = models.SlugField(blank=True, null=False, unique=True, verbose_name='Слаг')

    def __str__(self):
        return f'{self.name} по id: {self.pk}'

    def get_absolute_url(self):
        return reverse('phone', kwargs={'slug': self.slug})




