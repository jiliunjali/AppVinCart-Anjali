from django.urls import path
from .views import   CheckoutView, PaymentSuccessView, PayForCheckoutView #PayPageView, PaymentCancelledView, StripeWebhookView,PayementOfOrdersView, PaymentSuccessPageView
urlpatterns=[
    # path('payment/', PayPageView.as_view() ,name='pay_page'),
    path('payment_success/',PaymentSuccessView.as_view(),name='successful_payment_page'),
    # path('payment_cancelled/',PaymentCancelledView.as_view(),name='failed-canceled_payment_page'),
    # # Stripe webhook endpoint is a URL provided by your application that Stripe uses to send real-time notifications (webhooks) about events that occur in your Stripe account.
    # path('stripe_webhook/',StripeWebhookView.as_view(),name='stripe_webhook_endpoint'),
    # path('payment_intent/',PayementOfOrdersView.as_view(),name='payment_intent'),
    # path('intent_payment_success/',PaymentSuccessPageView.as_view(),name='intent_payment_success'),
    path('checkout/<int:user_id>', CheckoutView.as_view(), name='checkout'),
    path('pay_for_checkout/<int:user_id>', PayForCheckoutView.as_view(), name='pay_for_checkout'),
    
    
    
    
]