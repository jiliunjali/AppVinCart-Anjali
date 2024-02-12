from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView
from authapp.models import User
from django.core.exceptions import ObjectDoesNotExist

from productapp.models import Product
from .models import Order, FeedBack
from cartapp.models import Cart, CartItems
from cartapp.views import AddToCartView


class DisplayOrderContentsView(View):
    def get(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            orders = Order.objects.filter(user_id=user_id)
            # for total price for each order item
            for order in orders:
                total_amount = Decimal(0)
                cart_items = order.cart.cart_items.all()  # to access related CartItems
                for cart_item in cart_items:
                    # for total amount for each cart item
                    total_amount += Decimal(cart_item.products.price * cart_item.quantity * (1 - (cart_item.products.discount / 100)))
                order.total_amount = total_amount
            total_price = sum(order.total_amount for order in orders)

            return render(request, 'order_contents.html', {'orders': orders, 'total_price': total_price})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User orders not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

#little issue here, since cart is being used so , it is taking the whole cart to make order
class AddProductToOrderView(View):
    def post(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            product_id = kwargs.get('product_id')
            # Retrieve the user instance
            user = User.objects.get(pk=user_id)
            product = get_object_or_404(Product, id=product_id)
            # Retrieve the user's cart
            cart = Cart.objects.get(user=user)
            # Create or get the cart item for the product
            cart_item, created = CartItems.objects.get_or_create(cart=cart, products=product)
            
            total_amount = product.price * (1 - (product.discount / 100))
            order = Order.objects.create(user_id=user, cart=cart, total_amount=total_amount)
            order.save()
            return JsonResponse({'message': 'Order is placed. Check your orders.'}, status=201)
        except Product.DoesNotExist:
            return HttpResponse("Error: Product does not exist")
        except Exception as e:
            return HttpResponse(f"Error: {e}")

class AddCartToOrderView(View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = User.objects.get(pk=user_id)
        cart_items = CartItems.objects.filter(user=user)
        # Logic to add cart contents to order table
        for item in cart_items:
            order = Order.objects.create(user_id=user, product_id=item.products, quantity=item.quantity)
            order.save()
        return redirect('order_contents')

class DeleteOrderView(View):
    def post(self, request, *args, **kwargs):
        try:
            order_id = kwargs.get('order_id')
            order = Order.objects.get(id=order_id)
            order.delete()
            return JsonResponse({'message': 'Order is successfully removed. Check your updates.'}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Order not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
class FeedBackView(ListView):
    model = FeedBack
    template_name = 'feedback_list.html'
    context_object_name = 'feedbacks'
    
    
