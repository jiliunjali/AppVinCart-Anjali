from django.contrib import admin

from .models import FeedBack, Order

# Register your models here.
admin.site.register(Order)
admin.site.register(FeedBack)
