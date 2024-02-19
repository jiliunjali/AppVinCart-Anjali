from django.db import models
from paymentapp.models import Payment
from authapp.models import User
from productapp.models import Product
# from cartapp.models import Cart

from datetime import datetime, timedelta, timezone
import random

rating_choices = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

# Create your models here.
class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    # cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ManyToManyField(Product, related_name='orders')
    total_amount = models.DecimalField(max_digits=10,decimal_places=2, default =0)
    estimated_delivery_date = models.DateField(blank = True, default=(datetime.now().date()+timedelta(6)))
    payment = models.ForeignKey(Payment, on_delete = models.SET_NULL, null=True, related_name='order')
    
    # def save(self, *args, **kwargs):
    #     if not self.estimated_delivery_date:
    #         today=datetime.now().date()
    #         random_days= random.randint(2,5)
    #         self.estimated_delivery_date = today + timedelta(days=random_days)
            
    #     total = sum(product.price * (1 - (product.discount / 100)) for product in self.product.all())
    #     self.Total_amount = total    
    #     super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        if not self.estimated_delivery_date:
            self.estimated_delivery_date = timezone.now() + timezone.timedelta(random.randint(2, 5))

        super().save(*args, **kwargs)

        # # Calculate total_amount after saving the instance
        # total_amount = sum(prod.price * (1 - (prod.discount / 100)) for prod in self.product.all())
        # self.total_amount = total_amount
        # self.save(update_fields=['total_amount']) 
        
# to be filled when a user have received the delivered order
class FeedBack(models.Model):
    feedback = models.CharField(max_length = 500)
    rating_category = models.IntegerField(null = True, choices = rating_choices)
    product_id = models.ForeignKey(Product, related_name='feedbacks', on_delete=models.SET_NULL, null=True, blank=True)
    user_id = models.ManyToManyField(User, related_name='feedbacks')

# order and rating table will be here, rating will be asked when order is delivered for the feedback
# a user can rate multiple and a rate can have multiple users
# a product can have multiple ratings and a rating have multiple products
