from django import forms


class CalculatorForm(forms.Form):
    servings = forms.IntegerField(label='Порций', min_value=1, max_value=100)
