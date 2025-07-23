from django.shortcuts import render
from .models import *

# Create your views here.
def listCategory(request):
    category = Category.objects.all()

    context = {
        'title'     :'list category',
        'categories':category,
    }

    return render(request, 'inventory/category/list.html', context)

def addCategory(request):
    form = CotegoryForm(request.POST or None)
    if request.methode == "POST":
        if form.is_valid():
            form.save()
        return redirect('inventory:list_category')
    
    context = {
        'title':'Add New Category',
        'forms':form,
    }

    return render(request, 'inventory/category/create.html', context)