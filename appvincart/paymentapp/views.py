import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.views import View
import stripe
from django.views.decorators.csrf import csrf_exempt
from authapp.models import User
from orderapp.models import Order
from paymentapp.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

class CheckoutView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def get(self, request,*args,**kwargs):
    #     # Retrieve the PaymentIntent client secret (assuming it's passed as a query parameter)
    #     client_secret = request.GET.get('client_secret')
    #     client_secret = request.session.get('client_secret','')
    #     user_id = kwargs.get('user_id')
    #     user = User.objects.get(id=user_id)
    #     # orders = Order.objects.filter(id__in=request.session.get('order_ids', []))
    #     order_ids = request.session.get('order_ids', [])
    #     orders = Order.objects.filter(id__in=order_ids)
    #     print('********************************')
    #     print(orders)
    #     print(client_secret)
    #     total_amount = 0
    #     for order_id in order_ids:
    #             order = Order.objects.get(pk=order_id)
    #             products = order.product.all()  # Get all products related to the order
    #             # Calculate total amount for the order
    #             order_amount = sum(product.price for product in products)  # Amount in cents
    #             total_amount += order_amount
    #     context = {
    #         'client_secret': client_secret,
    #         'user': user,
    #         'orders': orders,
    #         'total_amount': total_amount,
    #     }
    #     return render(request, 'checkout.html',context)  #{'client_secret': client_secret}
    

    def post(self, request,*args,**kwargs):
        # data = request.POST  # or request.POST if your client sends form data
        user_id = kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        order_ids = request.POST.getlist('order_ids[]') 
        print(order_ids)# Get list of order IDs from the request
        currency = 'usd'   #data['currency']

        try:
            total_amount = 0  # Initialize total amount to 0
            payment_intent_items = []

            # Iterate over order IDs
            for order_id in order_ids:
                order = Order.objects.get(pk=order_id)
                products = order.product.all()  # Get all products related to the order
                # Calculate total amount for the order
                order_amount = sum(product.price for product in products)  # Amount in cents
                total_amount += order_amount  # Add order amount to total amount
                # Create payment intent items for each product in the order
                for product in products:
                    payment_intent_items.append({
                        'amount': product.price * 100,  # Amount in cents
                        'currency': currency,
                        'description': product.name,
                        'quantity': 1,  # Assuming quantity is 1 for each product
                    })
            print(payment_intent_items)
            # Now you can use the total amount to create the PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=int(float(total_amount) * 100),
                currency=currency,
                # customer: user.first_name,
                payment_method_types=['card'],
                description=f"Payment for multiple orders",
                automatic_payment_methods={"enabled": True},
                metadata={'order_ids': str(order_ids)},  # 'line_items':payment_intent_items
                

            )
            #Update is_paid field for corresponding payment
            payment = Payment.objects.create(user=user,amount_paid=total_amount, client_secret=payment_intent.client_secret)
            payment.is_paid = True
            payment.save()
            client_secret = payment_intent.client_secret
            request.session['order_ids'] = order_ids
            request.session['client_secret'] = payment_intent.client_secret
            # return JsonResponse({'client_secret': client_secret}, status=200)
            return redirect('pay_for_checkout', user_id=user_id)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=500)
        

class PayForCheckoutView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request,*args,**kwargs):
        # Retrieve the PaymentIntent client secret (assuming it's passed as a query parameter)
        client_secret = request.GET.get('client_secret')
        client_secret = request.session.get('client_secret','')
        user_id = kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        # orders = Order.objects.filter(id__in=request.session.get('order_ids', []))
        order_ids = request.session.get('order_ids', [])
        orders = Order.objects.filter(id__in=order_ids)
        print('********************************')
        print(orders)
        print(client_secret)
        total_amount = 0
        for order_id in order_ids:
                order = Order.objects.get(pk=order_id)
                products = order.product.all()  # Get all products related to the order
                # Calculate total amount for the order
                order_amount = sum(product.price for product in products)  # Amount in cents
                total_amount += order_amount
        context = {
            'client_secret': client_secret,
            'user': user,
            'orders': orders,
            'total_amount': total_amount,
        }
        return render(request, 'checkout.html',context) 



# from orderapp.models import Order
# from .models import Payment
# from django.views.decorators.csrf import csrf_exempt

# def create_payment_intent(amount, currency='usd'):
#     return stripe.PaymentIntent.create(
#         amount=amount,
#         currency=currency
#     )

# # Create your views here.
# class PayPageView(LoginRequiredMixin, ListView):
#     login_url = 'login'
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     def get(self, request, *args, **kwargs):
#         return render(request, 'payment_page.html')
#     def post(self, request, *args, **kwargs):
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price': settings.PRODUCT_PRICE,
#                     'quantity': 1,
#                 }
#             ],
#             mode = 'payment',
#             customer_creation='always',
#             success_url=settings.REDIRECT_DOMAIN + '/pay/payment_success?session_id={{CHECKOUT_SESSION_ID}}',
#             cancel_url=settings.REDIRECT_DOMAIN + '/pay/payment_cancelled',
#         )
#         return redirect(checkout_session.url, code=303)
    
class PaymentSuccessView(View):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    def post(self, request, *args, **kwargs):
        # checkout_session_id = request.GET.get('session_id', None)
        # session = stripe.checkout.Session.retrieve(checkout_session_id)
        # customer = stripe.Customer.retrieve(session.customer)
        # user_id = request.user.user_id
        # user_payment = Payment.objects.get(user=user_id)
        # user_payment.stripe_checkout_id = checkout_session_id
        # user_payment.save()
        return render(request, 'payment_success.html')

# class PaymentCancelledView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'payment_cancel.html')

# # this will be called by stripe when an event of interest have occured
# class StripeWebhookView(View):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     @csrf_exempt
#     def post(elf, request, *args, **kwargs):
#         time.sleep(10)
#         payload = request.body
#         signature_header = request.META['HTTP_STRIPE_SIGNATURE']
#         event = None
#         try:
#             event = stripe.Webhook.construct_event(
#                 payload, signature_header, settings.STRIPE_webhook_SECRET_TEST
#             )
#         except ValueError as e:
#             return HttpResponse(status=400)
#         except stripe.error.SignatureVerificationError as e:
#             return HttpResponse(status=400)
#         if event['type'] == 'checkout.session.completed':
#             session = event['data']['object']
#             session_id = session.get('id', None)
#             time.sleep(15)
#             user_payment = Payment.objects.get(stripe_checkout_id=session_id)
#             line_items = stripe.checkout.Session.list_list_items(session_id, limit=1)
#             user_payment.payment_bool = True
#             user_payment.save()
#         return HttpResponse(status=200)
    
# class PayementOfOrdersView(View):
    
#     def post(self, request, *args, **kwargs):
#         try:
#             # Set your Stripe API key
#             stripe.api_key = settings.STRIPE_SECRET_KEY

#             # Retrieve the order details from the database
#             user_id = request.user.id
#             order = Order.objects.filter(user_id=user_id).first()
            
#             if not order:
#                 return JsonResponse({'error': 'No order found for the user'}, status=400)

#             # Calculate the total amount for the order
#             total_amount = order.total_amount  # Adjust this based on your Order model structure
            
#             # Create a Payment Intent with the total amount
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=int(total_amount * 100),  # Convert to cents
#                 currency='usd',
#                 description='Payment for orders',
#                 payment_method_types= ['card'],
#                 customer=user_id,
#                 confirmation_method='manual',  # Set confirmation method to manual
#                 return_url='https://127.0.0.1/pay/intent_payment_success/'
#                 # Add more parameters as needed
#             )

#             # Return the client secret of the created Payment Intent
#             return JsonResponse({'client_secret': payment_intent.client_secret})

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
        
# class PaymentSuccessPageView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'payment_success.html')