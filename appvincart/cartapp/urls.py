from django.urls import path
from .views import CartView, AddToCartView, DeleteFromCartView, DeleteFromWishListView, TransferFromSaveForLaterToCartView, TransferToSaveForLaterView, WishListView

urlpatterns = [
    path('cart/<int:user_id>/', CartView.as_view(), name='cart'),
    path('wishlist/<int:user_id>/', WishListView.as_view(), name='wishlist'),
    path('add/<int:user_id>/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete/<int:user_id>/<int:product_id>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('transfer/<int:user_id>/<int:product_id>/', TransferToSaveForLaterView.as_view(), name='transfer_to_save_for_later'),
    path('delete_wishlist/<int:user_id>/<int:product_id>/', DeleteFromWishListView.as_view(), name='delete_from_wishlist'),
    path('transfer_to_cart/<int:user_id>/<int:product_id>/', TransferFromSaveForLaterToCartView.as_view(), name='transfer_to_cart'),
]