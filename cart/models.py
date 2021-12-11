from django.db import models
from django.contrib.auth.models import User

from shop.models import Product

from datetime import datetime


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cart')
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username +"'s cart"

    def getItems(self):
        #get all items in the user's cart
        #give zero on user login    
        try:
            cart_items = self.cart_items.all()
            total = 0
            for cart_item in cart_items:
                total += cart_item.quantity
            return total
        except:
            return 0 


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='cart_items')

    def __str__(self):
        return self.product.name+' item'
     