from inventory.forms import CategoryForm
from inventory.models import Category
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView


class CategoryListView(ListView):
    model = Category
    template_name = "inventory/category/list.html"

    def get_context_data(self, **kwrags):
        context = super().get_context_data(**kwrags)
        context['title']="List Category"
        return context


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "inventory/category/create.html"
    success_url = reverse_lazy('inventory:category_list')

    def get_context_data(self, **kwrags):
        context = super().get_context_data(**kwrags)
        context['title']="Create Category"
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "inventory/category/create.html"
    success_url = reverse_lazy('inventory:category_list')

    def get_context_data(self, **kwrags):
        context = super().get_context_data(**kwrags)
        context['title']="Update Category"
        return context