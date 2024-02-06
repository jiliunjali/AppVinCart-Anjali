from django.urls import path
from . import views

urlpatterns=[
    path('',views.Home.as_view(), name='home'),
    path('product/<int:pk>/',views.ProductDetail.as_view(), name='productdetail'),
    
    
]
