from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework.response import Response
from authapp.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from django.db import transaction



from productapp.models import Product
from .models import Cart, CartItems, SaveForLater


# Create your views here.

class CartView(LoginRequiredMixin,View):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')  
        cart = get_object_or_404(Cart, user_id=user_id)
        cart_items = cart.cart_items.select_related('products')
        context = {}
        if cart_items.exists():
            context['cart_items'] = cart_items
        else:
            context['cart_empty'] = True
        return render(request, self.template_name, context)
    
class WishListView(LoginRequiredMixin,View):
    
    template_name = 'wishlist.html'
    
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        wish_cart = get_object_or_404(SaveForLater, user_id = user_id)
        cart_items = wish_cart.products_id.all()
        context = {}
        if cart_items.exists():
            context['cart_items'] = cart_items
        else:
            context['cart_empty'] = True
        return render(request, self.template_name, context)
        
    

class AddToCartView(LoginRequiredMixin,View):

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        product_id = kwargs.get('product_id')
        quantity = int(request.POST.get('quantity', 1)) # default to 1
        
        # Retrieve the user instance corresponding to the user_id
        user = get_object_or_404(User, id=user_id)
        
        product = get_object_or_404(Product, id=product_id)
        
        # Get the cart associated with the user or create a new one if it doesn't exist
        cart, created = Cart.objects.get_or_create(user=user)
        # Get the cart item associated with the product or create a new one if it doesn't exist
        cart_item, created = CartItems.objects.get_or_create(cart=cart, products=product)
        if not created:
            # If the cart item already exists, update its quantity by incrementing it by the specified amount
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({'message': 'Product added to cart.'}, status=201)
        
        
#delete is not just decreasing the quantity but also delteing the product from the cart
class DeleteFromCartView(LoginRequiredMixin,View):

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        product_id = kwargs.get('product_id')
        
        cart = get_object_or_404(Cart, user_id=user_id)
        # Retrieve the product instance corresponding to the product_id
        product = get_object_or_404(Product, id=product_id)
        cart_item = get_object_or_404(CartItems, cart=cart, products=product_id)
        quantity = cart_item.quantity
        cart_item.delete()
        # Increase the product quantity back by the same amount that was removed from the cart
        product.quantity += quantity
        product.save()
        
        return JsonResponse({'message': 'Product removed from cart.'}, status=200)
    
class TransferToSaveForLaterView(View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        product_id = kwargs.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        user = get_object_or_404(User, id=user_id)
        product = get_object_or_404(Product, id=product_id)

        # Get the Cart instance associated with the user
        cart = get_object_or_404(Cart, user=user)

        # Get the CartItems instance for the specified product in the cart
        cart_item = get_object_or_404(CartItems, cart=cart, products=product)

        # Add the product to the SaveForLater model
        save_for_later, created = SaveForLater.objects.get_or_create(user_id=user)
        save_for_later.products_id.add(product)

        # Increase the quantity of the product in the Product model
        product.quantity += cart_item.quantity
        product.save()

        # Delete the CartItems instance for the product in the cart
        cart_item.delete()

        return JsonResponse({'message': 'Product transferred to Save For Later'}, status=201)
