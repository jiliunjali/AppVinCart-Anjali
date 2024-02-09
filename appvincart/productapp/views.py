from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product

# Create your views here.
class Home(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products' # name under which queryset will be available in the template
    
    def get_queryset(self):
        # Sort by new arrival (newest first)
        sort_by = self.request.GET.get('sort')
        if sort_by == 'new_arrival':
            queryset = Product.objects.order_by('-id')
        elif sort_by == 'from_oldest':
            queryset = Product.objects.order_by('id')
        elif sort_by == 'price_max_to_low':
            queryset = Product.objects.order_by('-price')
        elif sort_by == 'price_low_to_max':
            queryset = Product.objects.order_by('price')
        else:
            queryset = Product.objects.all()
        return queryset
    
class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'

#extra view added to make search bar reactive if possible
class ProductFilterView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 10  # Optional: Set the number of products per page

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')  # Get the search query from the request
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset