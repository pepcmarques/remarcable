from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Product, Category, Tag 
from .forms import ProductSearchForm
from .services import search_products


app_name = 'core'

def search(request):
    form = ProductSearchForm(request.POST or None)
    
    if form.is_valid():
        products = search_products(form.cleaned_data)
    else:
        products = Product.objects.all().order_by('name')
    
    # Pagination (assuming you have it)
    paginator = Paginator(products, 10)  # 10 products per page
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    return render(request, 'core/search.html', {'form': form, 'page_obj': page_object})


def about(request):
    return render(request, f'{app_name}/about.html')


def contact(request):
    return render(request, f'{app_name}/contact.html')
