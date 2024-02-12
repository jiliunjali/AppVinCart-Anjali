from django.urls import path
from .views import DisplayOrderContentsView, AddProductToOrderView, AddCartToOrderView, DeleteOrderView

urlpatterns = [
    path('contents/<int:user_id>/', DisplayOrderContentsView.as_view(), name='order_contents'),
    path('add/<int:user_id>/<int:product_id>/', AddProductToOrderView.as_view(), name='add_product_to_order'),
    path('add/cart/<int:user_id>/', AddCartToOrderView.as_view(), name='add_cart_to_order'),
    path('delete/<int:order_id>/', DeleteOrderView.as_view(), name='delete_order'),
]
