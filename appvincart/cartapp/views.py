from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework.response import Response
from authapp.models import User

from productapp.models import Product
from .models import Cart, SaveForLater


# Create your views here.

class CartView(View):
    template_name = 'cart.html'  # Specify the template name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id  # Assuming you have authenticated users
        cart_items = Cart.objects.filter(user_id=user_id)
        if cart_items.exists():
            context['cart_items'] = cart_items
        else:
            context['cart_empty'] = True
        return context
class AddToCartView(View):
    
    template_name ='cart.html'
    context_object_name = 'cart_items'
    
    def post(self, request, *args, **kwargs):
        user_id_ = request.data.get('user_id')
        product_id_ = request.data.get('product_id')
        quantity = request.data.get('quantity',1) # default to 1
        
        #if product_id or user_id is not correctly taken in request
        if not all[product_id_ , user_id_ ]:
            return JsonResponse({'error': 'User ID and Product ID are required.'}, status=400)
        
        # Retrieve the cart or create a new one if it doesn't exist
        cart, created =Cart.objects.get_or_create(user_id = user_id_)
        
        #checking for already existance of product in the cart
        if cart.products_id.filter(id=product_id_ ).exists():
            cart_item = cart.products_id.get(id=product_id_ )
            cart_item.quantity +=quantity
            cart_item.save()
            return JsonResponse({'message': 'Quantity updated in cart.'}, status=200)
        
        #if it is new item for cart of current user
        product = get_object_or_404(Product, id=product_id_ )
        cart.products_id.add(product, through_defaults={'quantity': quantity})
        return JsonResponse({'message': 'Product added to cart.'}, status=201)
    
class DeleteFromCartView(View):
    
    template_name ='cart.html'
    context_object_name = 'cart_items'
    
    def post(self, request, *args, **kwargs):
        user_id_ = request.data.get('user_id')
        product_id_ = request.data.get('product_id')
        
        #if product_id or user_id is not correctly taken in request
        if not all[product_id_ , user_id_ ]:
            return JsonResponse({'error': 'User ID and Product ID are required.'}, status=400)
        
        #retriving the product from the cart
        product = Cart.objects.get(id=product_id_ )
        
        #checking if product is in cart or not
        if not product.products_id.filter(id = product_id_ ).exists():
            return JsonResponse({'error': 'Product is not in the cart.'}, status=404)
        
        # if it exists in cart then remove it's quantity
        cart_item = product.product_id.get(id=product_id_ )
        quantity = cart_item.quantity
        product.product_id.remove(cart_item)
        
        #updating quantity in cart
        product.quantity -= quantity
        product.save()
        return JsonResponse({'message': 'Product removed from cart.'}, status=200)
    
class TransferToSaveForLaterView(View):
    
    template_name ='cart.html'
    context_object_name = 'cart_items'
    
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        # Validate user and product existence
        user = get_object_or_404(User, id=user_id)
        product = get_object_or_404(Product, id=product_id)
        
        # Check if the product is already in the Save For Later list for the user
        save_for_later, created = SaveForLater.objects.get_or_create(user_id=user_id)
        
        if not created and save_for_later.products_id.filter(id=product_id).exists(): #products_id is filed in the save for later
            # Update the quantity if the product already exists
            save_for_later.products_id.set([product_id])
            save_for_later.quantity = quantity
            save_for_later.save()
            return JsonResponse({'message': 'Product quantity updated in Save For Later'}, status=200)
        
        # Add the product to the Save For Later list
        save_for_later.products_id.add(product_id)
        save_for_later.quantity = quantity
        save_for_later.save()
        return JsonResponse({'message': 'Product added to Save For Later'}, status=201)