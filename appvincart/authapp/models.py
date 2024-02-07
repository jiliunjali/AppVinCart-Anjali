# from datetime import datetime
from django.db import models
import re
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

gender_choices=(
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    
)

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None, password2=None):
        if not email:
            raise ValueError("User must have a valid email address ")
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
        )
        
        user.set_password(password) # it will hash our password to save it # TODO problem in it's hashing to correct as i can't see it in admin(problem is only for user not for superuser)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, password=None):
        
        user=self.create_user(
            email = email,
            first_name =first_name,
            password = password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
# absractuser can be used too where password will be automatically handled by AbstractUser
class User(AbstractBaseUser):
    
    # def validate_password(value):
    #     password_regex = re.compile(r'^[A-Za-z0-9@_]{8,}$')
    #     if not password_regex.match(value):
    #         raise Exception("Password must be at least 8 characters long and contain only alphanumeric characters, '@', or '_'")

    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=False, unique=True)
    phone = models.CharField(max_length= 15)
    address = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=gender_choices)
    # Password = models.CharField(max_length=50,validators=[validate_password])
    registered_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False) #TODO :role table with id here
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name'] #['First_Name','Password']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
        "Does user have permissions to view the app 'app_label'?"
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    
    
# -- TODO: need to encrupt the passwords using a algo... any
