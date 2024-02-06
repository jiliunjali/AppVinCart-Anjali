from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.registration,name='registration'),
    path('login/',views.login.as_view(),name='login'),
    path('forgetpass/',views.forget_password,name='forget_password'),
    path('resetpass/',views.reset_password,name='reset_password'),

]