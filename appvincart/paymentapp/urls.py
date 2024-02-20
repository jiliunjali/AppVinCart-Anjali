from django.urls import path
from .views import   CheckoutView, PaymentSuccessView, PayForCheckoutView, PaymentListView, PaymentRefundView
urlpatterns=[
    # path('payment/', PayPageView.as_view() ,name='pay_page'),
    path('payment_success/<int:payment_id>/',PaymentSuccessView.as_view(),name='successful_payment_page'),
    # path('payment_cancelled/',PaymentCancelledView.as_view(),name='failed-canceled_payment_page'),
    path('checkout/<int:user_id>', CheckoutView.as_view(), name='checkout'),
    path('pay_for_checkout/<int:user_id>', PayForCheckoutView.as_view(), name='pay_for_checkout'),
    path('payments_display/<int:user_id>', PaymentListView.as_view(), name='payments_display'),
    path('payment_refund/<int:user_id>', PaymentRefundView.as_view(), name='payment_refund'),
    
    
    
    
    
    
]