from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product

# Create your views here.
class Home(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products' # name under which queryset will be available in the template
    
    def get_queryset(self):
        # Add a minus sign (-) to indicate descending order (newest first)
        queryset = Product.objects.order_by('-id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context for sorting by price
        context['products_by_price'] = Product.objects.order_by('price')
        return context
    
class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'
