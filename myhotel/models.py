from django.db import models

class User(models.Model):
    hotel_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=255)
    alternate_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=250,null=True)
    password = models.CharField(max_length=128)  # You might want to use Django's built-in authentication system instead
    valid_upto = models.DateField()
    payment = models.CharField(max_length=100)
    details = models.TextField()
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.hotel_name
class items(models.Model):
    hotel_id=models.BigIntegerField(default=0)
    Item_Name=models.CharField(max_length=100)
    unit_Price=models.FloatField()


class Customer(models.Model):
    hotel_id=models.BigIntegerField()
    table_no=models.BigIntegerField()
    customer_name=models.CharField(max_length=250,null=True)
    customer_mobile_number=models.CharField(max_length=250,null=True)

class bill(models.Model):
    hotel_id=models.BigIntegerField()
    table_no=models.BigIntegerField()
    Item_Name=models.CharField(max_length=100,null=True)
    unit_Price=models.FloatField()
    quantity=models.FloatField()
    Total=models.FloatField()

class collection(models.Model):
    hotel_id=models.BigIntegerField()
    table_no=models.BigIntegerField()
    Customer_name=models.CharField(max_length=100,null=True)
    mobile=models.CharField(max_length=100,null=True)
    Total=models.FloatField()
    date=models.DateField()

class inquiry(models.Model):
    mobile=models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)


