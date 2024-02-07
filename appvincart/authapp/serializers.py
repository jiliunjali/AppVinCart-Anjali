from rest_framework import serializers
from  .models import User
#serializers are like modelform

# it needed to be mentioned in user's view as the data will be first fetched there only
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'},write_only = True) 
    class Meta:
        model = User
        # fields = '__all__' # all what we what needed to be mentioned in create_user method of usermanager
        fields = ['email', 'first_name', 'password', 'password2'] # TODO for all columns in user that we want we need to provide then in create_user method of user_manager to enable the working
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
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    class Meta:
        fields = ['email']
        
    def validate(self, data):
        pass
        