from django.urls import path
from .views import SendPasswordResetEmailView, UserChangePasswordView, UserPasswordResetView, UserProfileView, UserRegisterationView, UserLoginView

urlpatterns=[
    # path('register/',views.registration,name='registration'),
    # path('login/',views.login.as_view(),name='login'),
    # path('forgetpass/',views.forget_password,name='forget_password'),
    # path('resetpass/',views.reset_password,name='reset_password'),
    path('register/', UserRegisterationView.as_view() ,name='register'),
    path('login/', UserLoginView.as_view() ,name='login'),
    path('profile/', UserProfileView.as_view() ,name='profile'),
    path('changepassword/', UserChangePasswordView.as_view() ,name='changepassword'),
    path('resetforgotpassword/',SendPasswordResetEmailView.as_view(), name='reset_forgot_password'),
    path('resetpassword/<uid>/<token>/',UserPasswordResetView.as_view(), name='reset_password'), # adding slash at the ed of writting this url is really important, although automatically adds a slash at the end ; but that's troublesome too.
]