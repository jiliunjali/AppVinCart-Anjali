from django.db import models
from authapp.models import User
from productapp.models import Product
from cartapp.models import Cart

from datetime import datetime, timedelta
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
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2, default =0)
    estimated_delivery_date = models.DateField(blank = True, default=(datetime.now().date()+timedelta(6)))
    
    def save(self, *args, **kwargs):
        if not self.estimated_delivery_date:
            today=datetime.now().date()
            random_days= random.randint(2,5)
            self.estimated_delivery_date = today + timedelta(days=random_days)
            
        # for o in self.order.products.Price:  # it can't be done as product inside cart is not a single product but in a many to many relation field rather than queryset, so we need to iterate ovr it to get data
        total = sum(item.products.price for item in self.cart.cart_items.all())
        self.Total_amount = total    
        super().save(*args, **kwargs)
        
# to be filled when a user have received the delivered order
class FeedBack(models.Model):
    feedback = models.CharField(max_length = 500)
    rating_category = models.IntegerField(null = True, choices = rating_choices)
    product_id = models.ForeignKey(Product, related_name='feedbacks', on_delete=models.SET_NULL, null=True, blank=True)
    user_id = models.ManyToManyField(User, related_name='feedbacks')

# order and rating table will be here, rating will be asked when order is delivered for the feedback
# a user can rate multiple and a rate can have multiple users
# a product can have multiple ratings and a rating have multiple products
