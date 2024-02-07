from django.urls import path
from .views import UserChangePasswordView, UserProfileView, UserRegisterationView, UserLoginView

urlpatterns=[
    # path('register/',views.registration,name='registration'),
    # path('login/',views.login.as_view(),name='login'),
    # path('forgetpass/',views.forget_password,name='forget_password'),
    # path('resetpass/',views.reset_password,name='reset_password'),
    path('register/', UserRegisterationView.as_view() ,name='register'),
    path('login/', UserLoginView.as_view() ,name='login'),
    path('profile/', UserProfileView.as_view() ,name='profile'),
    path('changepassword/', UserChangePasswordView.as_view() ,name='changepassword'),
    
    
    
    

]