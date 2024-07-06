from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст', blank=True,)
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)
    tag = models.ManyToManyField('Tag', blank=True, related_name='tags', verbose_name='Теги', through='Scope')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Scope(models.Model):
    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='scope', verbose_name='новость')
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, related_name='scope', verbose_name='тег')
    is_main = models.BooleanField(default=False, verbose_name='основной?')

