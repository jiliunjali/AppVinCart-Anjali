from datetime import datetime
from django.db import models
import re

gender_choices=(
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    
)

# Create your models here.
# absractuser can be used too where password will be automatically handled by AbstractUser
class User(models.Model):
    
    def validate_password(value):
        password_regex = re.compile(r'^[A-Za-z0-9@_]{8,}$')
        if not password_regex.match(value):
            raise Exception("Password must be at least 8 characters long and contain only alphanumeric characters, '@', or '_'")

    First_Name = models.CharField(max_length=50, null=False)
    Last_Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100, null=False)
    Phone = models.CharField(max_length= 15)
    Address = models.CharField(max_length=200)
    Gender = models.CharField(max_length=1, choices=gender_choices)
    Password = models.CharField(max_length=50,validators=[validate_password])
    # TimeOfRegister = models.DateTimeField(default='YYYY-MM-DDTHH:MM:SS')
    
    
