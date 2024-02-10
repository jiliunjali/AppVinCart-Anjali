from django.urls import path
from .views import CartView, AddToCartView, DeleteFromCartView, TransferToSaveForLaterView, WishListView

urlpatterns = [
    path('cart/<int:user_id>/', CartView.as_view(), name='cart'),
    path('wishlist/<int:user_id>/', WishListView.as_view(), name='wishlist'),
    path('cart/add/<int:user_id>/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/delete/<int:user_id>/<int:product_id>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('cart/transfer/<int:user_id>/<int:product_id>/', TransferToSaveForLaterView.as_view(), name='transfer_to_save_for_later'),
]