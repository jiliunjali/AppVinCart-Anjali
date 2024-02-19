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

from django.db import transaction


class DisplayOrderContentsView(View):
    def get(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            orders = Order.objects.filter(user_id=user_id)
            # for total price for each order item
            for order in orders:
                total_amount = Decimal(0)
                products = order.product.all()
                for product in products:
                    total_amount += Decimal(product.price * (1 - (product.discount / 100)))
                order.total_amount = total_amount
            total_price = sum(order.total_amount for order in orders)

            return render(request, 'order_contents.html', {'orders': orders, 'total_price': total_price})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User orders not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

#little issue here, since cart is being used so , it is taking the whole cart to make order
# class AddProductToOrderView(View):
#     def post(self, request, *args, **kwargs):
#         try:
#             user_id = kwargs.get('user_id')
#             product_id = kwargs.get('product_id')
#             # Retrieve the user instance
#             user = User.objects.get(pk=user_id)
#             product = get_object_or_404(Product, id=product_id)
#             # Retrieve the user's cart
#             cart = Cart.objects.get(user=user)
#             # Create or get the cart item for the product
#             cart_item, created = CartItems.objects.get_or_create(cart=cart, products=product)
            
#             total_amount = product.price * (1 - (product.discount / 100))
#             order = Order.objects.create(user_id=user, cart=cart, total_amount=total_amount)
#             order.save()
#             return JsonResponse({'message': 'Order is placed. Check your orders.'}, status=201)
#         except Product.DoesNotExist:
#             return HttpResponse("Error: Product does not exist")
#         except Exception as e:
#             return HttpResponse(f"Error: {e}")

# class AddCartToOrderView(View):
#     def post(self, request, *args, **kwargs):
#         try:
#             user_id = kwargs.get('user_id')
#             user = User.objects.get(pk=user_id)
#             cart = Cart.objects.get(user=user)
#             cart_items = CartItems.objects.filter(cart=cart)
#             for cart_item in cart_items:
#                 order = Order.objects.create(
#                     user_id=user,
#                     cart=cart,
#                     total_amount=cart_item.products.price * cart_item.quantity * (1 - (cart_item.products.discount / 100))
#                 )
#             return JsonResponse({'message': 'Orders are placed. Check your orders.'}, status=201)
#         except Cart.DoesNotExist:
#             return HttpResponse("Error: Cart does not exist")
#         except Exception as e:
#             return HttpResponse(f"Error: {e}")
        
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
        
# class AddToOrderView(View):
#     def post(self, request, *args, **kwargs):
#         try:
#             user_id = kwargs.get('user_id')
#             product_ids = request.POST.getlist('product_ids[]')
#             # Retrieve the user instance
#             user = User.objects.get(pk=user_id)
#             order = Order.objects.create(user_id=user)
#             # Add all selected products to the order
#             total_amount = 0
#             for product_id in product_ids:
#                 product = get_object_or_404(Product, id=product_id)
#                 total_amount += product.price * (1 - (product.discount / 100))
#                 order.product.add(product)
#             order.total_amount = total_amount
#             order.save()
#             return JsonResponse({'message': 'Order is placed. Check your orders.'}, status=201)
#         except Product.DoesNotExist:
#             return HttpResponse("Error: Product does not exist")
#         except Exception as e:
#             return HttpResponse(f"Error: {e}")
        
# from django.db import transaction

class AddToOrderView(View):
    def post(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            product_ids = request.POST.getlist('product_ids[]')

            # Retrieve the user instance
            user = User.objects.get(pk=user_id)

            # Start a database transaction
            with transaction.atomic():
                # Create the Order instance
                order = Order.objects.create(user_id=user)

                # Add all selected products to the order
                total_amount = 0
                for product_id in product_ids:
                    product = get_object_or_404(Product, id=product_id)
                    total_amount += product.price * (1 - (product.discount / 100))
                    order.product.add(product)

                # Update the total_amount field
                order.total_amount = total_amount

                # Save the Order instance
                order.save()

            return JsonResponse({'message': 'Order is placed. Check your orders.'}, status=201)

        except Product.DoesNotExist:
            return HttpResponse("Error: Product does not exist")

        except Exception as e:
            return HttpResponse(f"Error: {e}")


