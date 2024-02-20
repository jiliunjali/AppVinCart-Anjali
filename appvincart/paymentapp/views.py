import time
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
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
    
    def get(self, request,*args,**kwargs):
        user_id = kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        order_ids = request.GET.getlist('order_ids[]') 
        orders = Order.objects.filter(id__in=request.session.get('order_ids', []))
        total_amount = 0
        for order_id in order_ids:
            order = Order.objects.get(pk=order_id)
            products = order.product.all()
            order_amount = sum(product.price for product in products)
            total_amount += order_amount
        context = {
                'user': user,
                'orders': orders,
                'total_amount': total_amount,
            }
        request.session['order_ids'] = order_ids
        return render(request, 'proceed_checkout.html',context)

    def post(self, request,*args,**kwargs):
        user_id = kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        order_ids = request.session.get('order_ids', [])
        payment_method_id = request.POST.get('paymentMethodId')
        currency = 'usd'
        shipping_name = request.POST.get('shippingName')  # Retrieve shipping name from request
        shipping_address = request.POST.get('shippingAddress')
        shipping_city = request.POST.get('shippingCity')
        shipping_country = request.POST.get('shippingCountry')
        shipping_state = request.POST.get('shippingState')

        try:
            total_amount = 0 
            payment_intent_items = []

            # Iterate over order IDs
            for order_id in order_ids:
                order = Order.objects.get(pk=order_id)
                products = order.product.all()  # Get all products related to the order
                # Calculate total amount for the order
                order_amount = sum(product.price for product in products)
                total_amount += order_amount  # Add order amount to total amount
                # Create payment intent items for each product in the order
                for product in products:
                    payment_intent_items.append({
                        'amount': product.price * 100,  # Amount in cents
                        'currency': currency,
                        'description': product.name,
                        'quantity': 1, 
                    })
            print(payment_intent_items)
            # Create or retrieve a customer in Stripe
            customer = stripe.Customer.create(
                name=user.first_name,
                email=user.email,
            )
            
            # Attach the PaymentMethod to the customer
            stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer.id
            )
            
            # Modify the billing details of the PaymentMethod
            stripe.PaymentMethod.modify(
                payment_method_id,
                billing_details={
                    'name': shipping_name,
                    'address': {
                        'line1': shipping_address,
                        "city": shipping_city,
                        "country": shipping_country,
                        "state": shipping_state
                    }
                }
            )
            
            # Now you can use the total amount to create the PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=int(float(total_amount) * 100),
                currency=currency,
                customer=customer.id,
                payment_method=payment_method_id,
                description=f"Payment for multiple orders: {payment_method_id}",
                # automatic_payment_methods={"enabled": True},
                metadata={'order_ids': str(order_ids)},
            )

            #Update is_paid field for corresponding payment
            payment = Payment.objects.create(user=user,amount_paid=total_amount, client_secret=payment_intent.client_secret)
            payment.save()
            client_secret = payment_intent.client_secret
            request.session['order_ids'] = order_ids
            request.session['client_secret'] = payment_intent.client_secret
            request.session['payment_id']= payment.id
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
        client_secret = request.session.get('client_secret','')
        payment_id = request.session.get('payment_id',0)
        user_id = kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        orders = Order.objects.filter(id__in=request.session.get('order_ids', []))
        order_ids = request.session.get('order_ids', [])
        orders = Order.objects.filter(id__in=order_ids)
        print('********************************')
        print(orders)
        print(client_secret)
        total_amount = 0
        for order_id in order_ids:
                order = Order.objects.get(pk=order_id)
                products = order.product.all()
                # Calculate total amount for the order
                order_amount = sum(product.price for product in products)
                total_amount += order_amount
        context = {
            'client_secret': client_secret,
            'user': user,
            'orders': orders,
            'total_amount': total_amount,
            'payment_id': payment_id
        }
        return render(request, 'checkout.html',context) 

class PaymentSuccessView(View):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    def get(self, request, *args, **kwargs):
        payment_id = kwargs.get('payment_id')
        payment = get_object_or_404(Payment, pk=payment_id)
        payment.is_paid = True
        payment.save()
        return render(request, 'payment_success.html')

# class PaymentCancelledView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'payment_cancel.html')

class PaymentRefundView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        client_secret = request.POST.get('payment_id')
        try:
            payment = Payment.objects.get(user=user_id, client_secret=client_secret)
        except Payment.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=404)
        try:
            # payment_intent = stripe.PaymentIntent.retrieve(client_secret)
            id = client_secret.split('_')[1]
            payment_intent_id='pi_'+id
            print(payment_intent_id)
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id,
                amount=int(payment.amount_paid),
            )
            return JsonResponse({'message': 'Refund successful'}, status=200)
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class PaymentListView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("User does not exist")
        payments = Payment.objects.filter(user=user, is_paid=True)
        return render(request, 'payment_display.html', {'payments': payments})
