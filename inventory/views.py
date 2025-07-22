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