# from django.shortcuts import render
# from django.contrib.auth.views import LoginView
# from .forms import RegistrationForm #LoginForm
# from django.shortcuts import redirect
# from .models import User

# # Create your views here.
# # registration, login, forgot password, reset password functionalities

# def registration(request):
#     # RegistrationView can be used to handle it all as well.
#     #create row in user table
#     form = RegistrationForm()
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#     context={"reg_form" : form}
#     return render(request,'registration.html', context)

# # def login(request):
# #     # lookup from user table
# #     # token will be generated here
# #     form = LoginForm()
# #     if request.method == 'POST':
# #         form = LoginForm(request.POST)
# #         if form.is_valid():
# #             form.save()
# #     context={"login_form":form}
# #     return render(request,'login.html', context)
# class login(LoginView):
#     model = User
#     template_name='login.html'

# def forget_password(request):
#     # for validation of email
#     return render(request,'forget_password.html')

# def reset_password(request):
#     # alter-update user table
#     return render(request, 'reset_password.html')

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SendPasswordResetEmailSerializer, UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer, UserChangePasswordSerializer
from django.contrib.auth  import authenticate
from .renderers import UserRenderer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_simplejwt.tokens import RefreshToken #for refresh token
from rest_framework.permissions import IsAuthenticated

# generating token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegisterationView(APIView):
    
    renderer_classes =[UserRenderer, TemplateHTMLRenderer]
    template_name = 'registration.html'
    
    def get(self, request, format=None):
        reg_form = UserRegistrationSerializer()
        return Response({'reg_form': reg_form}, template_name='registration.html')
    
    # we use post as user will give data to register himself , from here the request's data will be send to serializer
    def post(self, request, format = None):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token ,'msg':'Registration Successful'}, status = status.HTTP_201_CREATED) # status is 201 as data is being created
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
# TODO pass the custom error from view to user when a poblem occur in seralizer  -- the non field errors given to us in postman

#authentication is done here
class UserLoginView(APIView):
    
    renderer_classes =[UserRenderer]
    
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception = True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user=authenticate(email=email, password=password) # using these it will authenticate and check if there any user with it or not
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token ,'msg':'Login Success'}, status = status.HTTP_201_CREATED)
            else:
                return Response({'errors':{'non_field_errors': ['Email or Password is not valid']}}, status = status.HTTP_404_NOT_FOUND)
            

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated] # it is to tell that only authenticated users are allowded the profile view means , one needed to be a user, is authenticated was necessary otherwise it was throwing long Attribute-error rather than a error message that we are getting now.
    def get(self,request, format=None):
        serializer = UserProfileSerializer(request.user) # current user is send in request # we are getting this user via isauthenticated
        return Response(serializer.data, status = status.HTTP_200_OK)

#change_password requires token as it is done only after login and for login authentication is need to be done
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated] # to be authenticated and authorized , the token need with the request data
    def post(self, request, format =None):
        serializer = UserChangePasswordSerializer(data=request.data, context = {'user':request.user})
        if serializer.is_valid(raise_exception =True):
            return Response({'msg':'Password Changed Successfully'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset link is sent. please check your email'}, status = status.HTTP_200_Ok)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

