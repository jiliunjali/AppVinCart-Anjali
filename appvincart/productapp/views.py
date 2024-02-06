from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product

# Create your views here.
class Home(ListView):
    model = Product
    template_name = 'home.html'
    
class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'
