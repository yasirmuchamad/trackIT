from inventory.forms import CategoryForm
from inventory.models import Category
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView


class CategoryListView(ListView):
    model = Category
    template_name = "inventory/category/list.html"


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "inventory/category/create.html"
    success_url = reverse_lazy('item_list')

    