from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from recepis.calculator.forms import CalculatorForm

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)a
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }


def calculate(request, slug_recept):
    servings = int(request.GET.get('servings', 1))
    recipe = {ingredient: round(amount * servings, 3) for ingredient, amount in DATA[slug_recept].items()}
    name = slug_recept
    form = CalculatorForm
    context = {
        'title': name,
        'recipe': recipe,
        'form': form
    }
    return render(request, 'calculator/index.html', context)




