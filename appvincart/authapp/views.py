from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import RegistrationForm #LoginForm
from django.shortcuts import redirect
from .models import User

# Create your views here.
# registration, login, forgot password, reset password functionalities

def registration(request):
    # RegistrationView can be used to handle it all as well.
    #create row in user table
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
    context={"reg_form" : form}
    return render(request,'registration.html', context)

# def login(request):
#     # lookup from user table
#     # token will be generated here
#     form = LoginForm()
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             form.save()
#     context={"login_form":form}
#     return render(request,'login.html', context)
class login(LoginView):
    model = User
    template_name='login.html'

def forget_password(request):
    # for validation of email
    return render(request,'forget_password.html')

def reset_password(request):
    # alter-update user table
    return render(request, 'reset_password.html')
