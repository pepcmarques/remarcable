from django.urls import path, include
from api.views import product_search


urlpatterns = [
    path('search/', product_search, name='product-search'),
]