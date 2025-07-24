import openpyxl
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from inventory.forms import CategoryForm
from inventory.models import Category
from openpyxl.styles import Font, Alignment


##########################################################  views for category
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
    success_url = reverse_lazy('inventory:list_category')

    def get_context_data(self, **kwrags):
        context = super().get_context_data(**kwrags)
        context['title']="Update Category"
        return context


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "inventory/category/delete.html"
    success_url = reverse_lazy('inventory:list_category')

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        messages.success(self.request, f"Category '{category.name}' berhasil disimpan.")
        return super().delete(request, *args, **kwargs)
                                                    
def categoryToExcel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "List Category"

    # Judul besar di baris 1
    ws.merge_cells('A1:B1')  # gabungkan dari kolom A sampai B
    ws['A1'] = "List Category"
    ws['A1'].font = Font(size=14, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')

    # Header
    headers = ['Id', 'Name']
    ws.append(headers)

    # Data
    for idx, s in enumerate(Category.objects.all(), start=1):
        ws.append([
            idx,
            s.name,
        ])

    # Response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=category.xlsx'
    wb.save(response)
    return response

##########################################################  views for item

