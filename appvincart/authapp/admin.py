from django.contrib import admin
from .models import User, Role
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
class UserModelAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email", "first_name", "role_id"]
    list_filter = ["role_id"]
    fieldsets = [
        ("User_Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", 'last_name', 'phone', 'address', 'gender']}),
        ("Permissions", {"fields": ["role_id"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "first_name", "password1", "password2"],
            },
        ),
    ]
    
    def role_id(self, obj):
        return obj.role.name if obj.role else "No role"
    role_id.short_description = "Role"
    
    search_fields = ["email"]
    ordering = ["email","id"]
    filter_horizontal = []

# @admin.register(Role)
class RoleModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

# Now register the new UserAdmin and RoleAdmin...
admin.site.register(User, UserModelAdmin)
admin.site.register(Role, RoleModelAdmin)