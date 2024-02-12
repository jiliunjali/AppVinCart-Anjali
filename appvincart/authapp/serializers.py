#serializers are like modelform
from rest_framework import serializers
from  .models import User
#specially for reset password after forget password clicking  
from xml.dom import ValidationErr
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# it needed to be mentioned in user's view as the data will be first fetched there only
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'},write_only = True) 
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'address', 'gender', 'password', 'password2'] 
        extra_kwargs={
            'password': {'write_only': True}
        }
        
    #need to validate the data -- like password 1 and 2 are same or not
    def validate(self, data): # data from request in view to serializer is get in this data parameter
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return data
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 100)
    class Meta:
        model = User
        fields = ['email','password']
        
    # we will do authentication from view now , although we can do authentication from serializer too, but it can create problem at the time of token use and generation
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100,style={'input_type': 'password'},write_only = True)
    password2 = serializers.CharField(max_length=100,style={'input_type': 'password'},write_only = True)
    
    class Meta:
        fields = ['password', 'password2']
        
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return data
    
# for forget password
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    class Meta:
        fields = ['email']
        
    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists(): # check that email in user table have one of the email as one used by the the current user
            return data
        else:
            raise ValidationErr('You are not a Registered User')
        
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100,style={'input_type': 'password'},write_only = True)
    password2 = serializers.CharField(max_length=100,style={'input_type': 'password'},write_only = True)
    
    class Meta:
        fields = ['password', 'password2']
        
    def validate(self, data):
        try:
            password = data.get('password')
            password2 = data.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')      
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return data
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError('Token is not Valid or Expired')
        
