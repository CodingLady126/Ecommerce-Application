from django.db import models
from datetime import datetime    

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='products')
    price = models.IntegerField()
    details = models.TextField()
    date = models.DateTimeField(default=datetime.now, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='items')
    
    
   
    def __str__(self):
        return self.name
