
from django.db import models
from user.models import ProductInfo

class Cart(models.Model):
    cart_prd_quantity=models.BigIntegerField()
    cart_prd_id=models.ForeignKey(ProductInfo,on_delete=models.CASCADE)
    cart_total_price=models.BigIntegerField()
    user_id=models.BigIntegerField()
    

class Wishlist(models.Model):
    wishlist_prd_id=models.ForeignKey(ProductInfo,on_delete=models.CASCADE)
    user_id=models.BigIntegerField(default=0)
    
    
    