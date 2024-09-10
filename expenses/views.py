from django.views.generic.list import ListView
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from .forms import ExpenseSearchForm, CategoryForm
from .models import Expense, Category
from .reports import summary_per_category, total_spent


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            categories = form.cleaned_data.get('categories')

            if name:
                queryset = queryset.filter(name__icontains=name)
            if start_date:
                queryset = queryset.filter(date__gte=start_date)
            if end_date:
                queryset = queryset.filter(date__lte=end_date)
            if categories:
                queryset = queryset.filter(category__in=categories)

        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ExpenseSearchForm(self.request.GET)
        context['form'] = form
        context['summary_per_category'] = summary_per_category(self.get_queryset())
        context['total_spent'] = total_spent(self.get_queryset())
        queryset = self.get_queryset()
        monthly_summary = (
            queryset
            .annotate(year_month=TruncMonth('date'))
            .values('year_month')
            .annotate(total_amount=Sum('amount'))
            .order_by('year_month')
        )
        context['monthly_summary'] = monthly_summary
        
        return context

class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(expense_count=Count('expense'))
        return queryset

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_update.html'
    success_url = reverse_lazy('expenses:category-list')
