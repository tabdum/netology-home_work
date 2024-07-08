from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Article, Scope, Tag

from django.forms import BaseInlineFormSet


class ArticleTagInlineFormset(BaseInlineFormSet):
    def clean(self):
        if not any(form.cleaned_data.get('is_main') for form in self.forms):
            raise ValidationError('Укажите основной раздел')
        elif len(list(filter(lambda x: x.cleaned_data.get('is_main') is True, self.forms))) > 1:
            raise ValidationError('Основным может быть только один раздел')
        return super().clean()


class ArticleTagInline(admin.TabularInline):
    model = Scope
    extra = 3
    formset = ArticleTagInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # fields = ['title', 'text', 'published_at', 'image', 'tag']
    ordering = ['-published_at',]
    list_per_page = 10
    list_display = ['title', 'text', 'published_at', 'image']
    inlines = [ArticleTagInline, ]
    list_display_links = ['title']
    list_editable = ['text', 'published_at', 'image']
    list_filter = ['published_at', 'tag']



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', ]
    list_editable = ['name', ]
    list_display_links = ['pk', ]

