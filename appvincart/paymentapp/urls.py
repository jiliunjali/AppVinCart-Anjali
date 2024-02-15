from django.urls import path
from .views import PayPageView, PaymentCancelledView, PaymentSuccessView, StripeWebhookView
urlpatterns=[
    path('payment/', PayPageView.as_view() ,name='pay_page'),
    path('payment_success/',PaymentSuccessView.as_view(),name='successful_payment_page'),
    path('payment_cancelled/',PaymentCancelledView.as_view(),name='failed-canceled_payment_page'),
    # Stripe webhook endpoint is a URL provided by your application that Stripe uses to send real-time notifications (webhooks) about events that occur in your Stripe account.
    path('stripe_webhook/',StripeWebhookView.as_view(),name='stripe_webhook_endpoint'),
    
    
    
]