from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from authapp.models import User

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False) #to determine if payment is done making or not
    stripe_checkout_id = models.CharField(max_length=500)

#receiver is the decorator works on signal and sender(optional)-> on what signal this function , which is decorated is triggered
# this automated creation of payment instance to be created of registered user is necessary to mentain data integrity -> accuracy, consistency, and reliability of data stored in a database
@receiver(post_save, sender=User)    
def create_user_payment(sender, instance , created, **kwargs):
    if created:
        return Payment.objects.create(user=instance)