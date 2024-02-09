from django.db import models
from authapp.models import User
from productapp.models import Product

# Create your models here.
class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    products_id = models.ManyToManyField(Product)
    quantity = models.PositiveIntegerField(default = 1)
    
    # Product.Quantity = Product.Quantity - Quantity----- to be done in a view or so when the product is done ordering 
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        #iterating over each product and updating their quantity
        for product in self.product_id.all():
            if product.stock_status == 'IN_STOCK' :
                if product.quantity >= self.quantity:
                    product.quantity -= self.quantity
                    product.save()
                    
class SaveForLater(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    products_id = models.ManyToManyField(Product)
    quantity = models.PositiveIntegerField(default = 1)


    