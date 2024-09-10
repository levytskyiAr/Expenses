from django import forms
from .models import Expense
from .models import Category


class ExpenseSearchForm(forms.ModelForm):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}))
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),required=False,widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Expense
        fields = ('name', 'start_date', 'end_date', 'categories')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']