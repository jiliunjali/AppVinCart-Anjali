import time
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.views import View
import stripe
from .models import Payment
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class PayPageView(LoginRequiredMixin, ListView):
    login_url = 'login'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    def get(self, request, *args, **kwargs):
        return render(request, 'payment_page.html')
    def post(self, request, *args, **kwargs):
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': settings.PRODUCT_PRICE,
                    'quantity': 1,
                }
            ],
            mode = 'payment',
            customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + '/pay/payment_success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=settings.REDIRECT_DOMAIN + '/pay/payment_cancelled',
        )
        return redirect(checkout_session.url, code=303)
    
class PaymentSuccessView(View):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    def post(self, request, *args, **kwargs):
        checkout_session_id = request.GET.get('session_id', None)
        session = stripe.checkout.Session.retrieve(checkout_session_id)
        customer = stripe.Customer.retrieve(session.customer)
        user_id = request.user.user_id
        user_payment = Payment.objects.get(user=user_id)
        user_payment.stripe_checkout_id = checkout_session_id
        user_payment.save()
        return render(request, 'payment_success.html',{'customer': customer})

class PaymentCancelledView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'payment_cancel.html')

# this will be called by stripe when an event of interest have occured
class StripeWebhookView(View):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    @csrf_exempt
    def post(elf, request, *args, **kwargs):
        time.sleep(10)
        payload = request.body
        signature_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None
        try:
            event = stripe.Webhook.construct_event(
                payload, signature_header, settings.STRIPE_webhook_SECRET_TEST
            )
        except ValueError as e:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse(status=400)
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            session_id = session.get('id', None)
            time.sleep(15)
            user_payment = Payment.objects.get(stripe_checkout_id=session_id)
            line_items = stripe.checkout.Session.list_list_items(session_id, limit=1)
            user_payment.payment_bool = True
            user_payment.save()
        return HttpResponse(status=200)
