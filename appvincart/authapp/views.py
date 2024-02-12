from base64 import urlsafe_b64encode
from tokenize import TokenError
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import User
from .serializers import SendPasswordResetEmailSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer, UserChangePasswordSerializer #,LogOutSerializer
from django.contrib.auth  import authenticate
from .renderers import UserRenderer, SuccessRenderer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_simplejwt.tokens import RefreshToken  #for refresh token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from .utils import EmailUtils


# generating token manually - jwt token # HS256 the algo used in jwt token by default
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegisterationView(APIView):
    
    renderer_classes =[UserRenderer, SuccessRenderer, TemplateHTMLRenderer]
    template_name = 'registration.html'
    
    def get(self, request, format=None):
        reg_form = UserRegistrationSerializer()
        return Response({'reg_form': reg_form}, template_name=self.template_name)
    # we use post as user will give data to register himself , from here the request's data will be send to serializer
    def post(self, request, format = None):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            # return Response({'token':token ,'msg':'Registration Successful'}, status = status.HTTP_201_CREATED) # status is 201 as data is being created
            return redirect('login')
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#authentication is done here
class UserLoginView(APIView):
    
    renderer_classes =[UserRenderer, SuccessRenderer, TemplateHTMLRenderer]
    template_name = 'login.html'
    
    def get(self, request, format=None):
        login_form = UserLoginSerializer()
        return Response({'login_form': login_form}, template_name=self.template_name)
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        #for redirection to page with this url 
        if serializer.is_valid(raise_exception = True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            # using these it will authenticate and check if there any user with it or not
            user=authenticate(email=email, password=password) 
            if user is not None:
                token = get_tokens_for_user(user)
                #return Response({'token':token ,'msg':'Login Success'}, status = status.HTTP_201_CREATED)  # can be use to test if token is generated and what was the token
                return redirect('home')
            else:
                return Response({'errors':{'non_field_errors': ['Email or Password is not valid']}}, status = status.HTTP_404_NOT_FOUND)
            

class UserProfileView(APIView):
    renderer_classes = [UserRenderer, SuccessRenderer, TemplateHTMLRenderer]
    # it is to tell that only authenticated users are allowded the profile view means , one needed to be a user, is authenticated was necessary otherwise it was throwing long Attribute-error rather than a error message that we are getting now.
    permission_classes = [IsAuthenticated] 
    
    def get(self,request, format=None):
        # current user is send in request # we are getting this user via isauthenticated
        serializer = UserProfileSerializer(request.user) 
        return Response({"profile":serializer.data}, status = status.HTTP_200_OK, template_name='profile.html')



#change_password requires token as it is done only after login and for login authentication is need to be done
class UserChangePasswordView(APIView):
    
    renderer_classes = [UserRenderer, SuccessRenderer, TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated] # to be authenticated and authorized , the token need with the request data
    template_name = 'changepassword.html'
    
    def get(self, request, format=None):
        change_password_form = UserChangePasswordSerializer()
        return Response({'login_form': change_password_form}, template_name=self.template_name)
    
    def post(self, request, format =None):
        serializer = UserChangePasswordSerializer(data=request.data, context = {'user':request.user})
        if serializer.is_valid(raise_exception =True):
            return Response({'msg':'Password Changed Successfully'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
# for forget password
class SendPasswordResetEmailView(APIView):
    
    renderer_classes = [UserRenderer, SuccessRenderer]
    
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            uid = urlsafe_b64encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = f'http://localhost:3000/api/user/reset/{uid}/{token}'
            # Send email to user
            subject = 'Reset your password'
            message = f'Click the following link to reset your password: {link}'
            to_email = email
            EmailUtils.send_email(subject, message, to_email)
            return Response({'msg': 'Password reset link is sent. Please check your email'}, status=status.HTTP_200_OK)
            # return redirect('reset_password')   # -->  this redirect can be used in place of response in website
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#for updating the password passed by user after resetting forget password
class UserPasswordResetView(APIView):
    
    renderer_classes = [UserRenderer, SuccessRenderer]
    
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data = request.data, context={'uid':uid,'token':token })
        if serializer.is_valid(raise_exception =True):
            return Response({'msg':'Password is successfully reset'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"success": "User logged out successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)