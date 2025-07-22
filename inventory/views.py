from django.shortcuts import render

# Create your views here.
def listCategory(request):
    category = Category.objects.all()

    context = {
        'title'     :'list category',
        'categories':category,
    }

    return render(request, 'inventory/category/list.html', context)