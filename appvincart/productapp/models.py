from django.db import models
from authapp.models import User

from datetime import datetime, timedelta
import random



# Create your models here.

Rating_Choices = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

# especially use for product detail view
class Product(models.Model):
    Name = models.CharField(max_length=50, null=False)
    Image = models.ImageField(upload_to='images/',null=True, blank=True) # how to upload and save them
    Price = models.DecimalField(max_digits=10,decimal_places=2)
    Quantity = models.IntegerField()
    Stock_Status = models.CharField(default='OUT_OF_STOCK', max_length=12)
    Color = models.CharField(max_length = 20)
    Description = models.TextField(blank=True, max_length=500)
    Rating = models.IntegerField(choices = Rating_Choices)
    # Arrival = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Updating stock_status based on quantity
        if self.Quantity > 0:
            self.Stock_Status = 'IN_STOCK'
        else:
            self.Stock_Status = 'OUT_OF_STOCK'
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.Name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    products = models.ManyToManyField(Product)
    Quantity = models.PositiveIntegerField(default = 1)
    
    # Product.Quantity = Product.Quantity - Quantity----- to be done in a view or so when the product is done ordering 
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    order = models.OneToOneField(Cart, on_delete = models.CASCADE)
    Total_amount = models.DecimalField(max_digits=10,decimal_places=2, default =0)
    # Estimated_delivery_date = models.DateField(blank = True)
    
    def save(self, *args, **kwargs):
        # today=datetime.now().date()
        # random_days= random.randint(2,5)
        # self.Estimated_delivery_date = today + timedelta(days=random_days)
        # for o in self.order.products.Price:  # it can't be done as product inside cart is not a single product but in a many to many relation field rather than queryset, so we need to iterate ovr it to get data
        total = sum(product.Price for product in self.order.product.all())
        self.Total_amount = total    
        super().save(*args, **kwargs)
        
    
    
    
    
    
    
    
    
    
    
