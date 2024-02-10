from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from productapp.models import Product
from .models import Order
from cartapp.models import Cart, CartItems
from cartapp.views import AddToCartView


class DisplayOrderContentsView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        orders = Order.objects.filter(user_id=user_id)
        # Calculate total price for each order item
        for order in orders:
            total_amount = Decimal(0)
            cart_items = order.cart.cart_items.all()  # Access related CartItems
            for cart_item in cart_items:
                # Calculate total amount for each cart item
                total_amount += Decimal(cart_item.products.price * cart_item.quantity * (1 - (cart_item.products.discount / 100)))
            order.total_amount = total_amount
        total_price = sum(order.total_amount for order in orders)
        
        return render(request, 'order_contents.html', {'orders': orders, 'total_price': total_price})

# class AddProductToOrderView(View):
#     def post(self, request, *args, **kwargs):
#         # Retrieve the product_id from URL kwargs
#         product_id = kwargs.get('product_id')
        
#         # Create an instance of AddToCartView and call its post method to add the product to the cart
#         add_to_cart_view = AddToCartView()
#         add_to_cart_response = add_to_cart_view.post(request, *args, **kwargs)
        
#         # Check if the product was successfully added to the cart
#         if add_to_cart_response.status_code == 201:
#             # If successful, proceed to create an order
#             user_id = request.user.id
#             product_id = kwargs.get('product_id')
#             # Logic to add product to order table
#             order = Order.objects.create(user_id=user_id, product_id=product_id, quantity=1)
#             order.save()
            
#             # Redirect to the order contents page
#             return redirect('order_contents')
#         else:
#             # If adding to cart failed, handle the error accordingly
#             # For example, return an error response or redirect to a different page
#             return HttpResponse("Failed to add product to cart")

class AddProductToOrderView(View):
    def post(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            product_id = kwargs.get('product_id')
            # Retrieve the quantity from the request data
            quantity = 1 # int(request.POST.get('quantity', 1))
            # Retrieve the product
            product = get_object_or_404(Product, id=product_id)
            # Calculate the total amount with discount
            total_amount = product.price * quantity * (1 - (product.discount / 100))
            # Create the order
            order = Order.objects.create(user_id=user_id, product_id=product_id , total_amount=total_amount)
            order.save()
            # Redirect to the order contents page
            # return redirect('order_contents')
            return JsonResponse({'message': 'order is made , check the orders'}, status=201)
        except Product.DoesNotExist:
            return HttpResponse("Error: Product does not exist")
        except Exception as e:
            return HttpResponse(f"Error: {e}")

class AddCartToOrderView(View):
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        cart_items = CartItems.objects.filter(cart__user_id=user_id)
        # Logic to add cart contents to order table
        for item in cart_items:
            order = Order.objects.create(user_id=user_id, product_id=item.product_id, quantity=item.quantity)
            order.save()
        return redirect('order_contents')

class DeleteOrderView(View):
    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = Order.objects.get(id=order_id)
        # Logic to delete order and move data to save for later table
        # For example:
        order.delete()  # Delete the order
        # Move data to save for later table if needed
        return redirect('order_contents')
