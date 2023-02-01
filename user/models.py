from django.db import models

# Create your models here.


class UserInfo(models.Model):
    Name = models.CharField(max_length=20)
    username = models.CharField(max_length=10)
    email = models.EmailField()
    mobileno = models.BigIntegerField()
    password = models.TextField()
    isblocked = models.BooleanField(default=0)
    profile_pic = models.ImageField(default="", upload_to="img/")


class Coupon(models.Model):
    coupon_name = models.CharField(max_length=100, default="")
    offer = models.CharField(max_length=20, default="")


class Offer(models.Model):
    offer = models.CharField(max_length=20, default="")


class Category(models.Model):
    category_name = models.CharField(max_length=100, default="")
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    tot_num = models.BigIntegerField(default=0)


class ProductInfo(models.Model):
    product_name = models.CharField(max_length=100)
    product_image1 = models.ImageField(default="", upload_to="img/")
    product_image2 = models.ImageField(default="", upload_to="img/")
    product_image3 = models.ImageField(default="", upload_to="img/")
    product_image4 = models.ImageField(default="", upload_to="img/")
    product_price = models.BigIntegerField()
    product_description = models.TextField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=200, null=True)
    brand = models.CharField(default="", max_length=100)
    stock = models.BigIntegerField(default="0")
    offer_id = models.ForeignKey(Coupon, on_delete=models.CASCADE, default=1)


class AdminInfo(models.Model):
    Name = models.CharField(max_length=20)
    email = models.EmailField()
    mobileno = models.BigIntegerField()
    password = models.TextField()


class Brand(models.Model):
    Name = models.CharField(max_length=20, null=True)


class Adress(models.Model):
    Name = models.CharField(max_length=20)
    email = models.EmailField()
    mobileno = models.BigIntegerField()
    Lastname = models.CharField(max_length=20)
    Country = models.CharField(max_length=20)
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    Postcode = models.BigIntegerField()
    userid = models.BigIntegerField(default=0)


class Orderdetails(models.Model):
    address = models.ForeignKey(Adress,on_delete=models.CASCADE)
    order_prd_name = models.CharField(max_length=300)
    order_prd_price = models.BigIntegerField()
    order_prd_quantity = models.BigIntegerField()
    date = models.DateField()
    user_id = models.IntegerField()
    payment_method = models.CharField(max_length=20, default="")
    status = models.CharField(max_length=20, default="")
    order_prd_image = models.ImageField(default="", upload_to="img/")
    payment_status = models.CharField(max_length=50, default="")
    ord_id = models.CharField(max_length=200, default="")


class Coupon_details(models.Model):
    user_id = models.BigIntegerField()
    date = models.DateField()
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
