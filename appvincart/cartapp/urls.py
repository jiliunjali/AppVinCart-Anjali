from django.urls import path
from . import views

urlpatterns=[
    path('cart/<int:user_id>/',views.CartView.as_view(), name='cartlookup'),
    path('addtocart/<int:product_id>/<int:user_id>/',views.AddToCartView.as_view(), name='addtocart'),
    path('deletefromcart/',views.DeleteFromCartView.as_view(), name='deletefromcart'),
    path('saveforlater/',views.TransferToSaveForLaterView.as_view(), name='saveforlater'),

]