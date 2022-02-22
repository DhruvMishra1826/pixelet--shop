from django.db import models
from PIL import Image

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50,default="")
    subcategory = models.CharField(max_length=50,default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to = "shop/images",default="")
    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msgid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50,default="")
    subject = models.CharField(max_length=50,default="")
    text = models.CharField(max_length=500,default="")


    def __str__(self):
        return self.name
        

class Order(models.Model):
    order_id= models.AutoField(primary_key=True)
    items_json= models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zip_code=models.CharField(max_length=100)
    phone = models.CharField(max_length=111, default="")


class OrderUpdate(models.Model):
    update_id= models.AutoField(primary_key=True)
    order_id= models.IntegerField(default="")
    update_desc= models.CharField(max_length=5000)
    timestamp= models.DateField(auto_now_add= True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
