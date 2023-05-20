from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user_id = models.CharField(max_length=10)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    pfp = models.ImageField(upload_to='users0_pfp')
    otp = models.CharField(max_length=6)
    first_view = models.CharField(max_length=1,default=1)
    premium = models.BooleanField(default=False)
    join_date = models.CharField(max_length=255,default=0)
    free_end_date = models.CharField(max_length=255,default=0)
    first_login = models.BooleanField(default=False)
    theme_selection = models.CharField(default=0,max_length=2)
        
class Category(models.Model):
    user_id = models.CharField(max_length=10)
    category = models.CharField(max_length=255)
    
class Sales(models.Model):
    user_id = models.CharField(max_length=10)
    customer_name = models.CharField(max_length=255)
    order_name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    qty_weigth = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    date_of_delivery = models.CharField(max_length=255)
    time_of_delivery = models.CharField(max_length=255)
    extra_note = models.TextField()
    order_date = models.CharField(max_length=255)
    
class Expense(models.Model):
    user_id = models.CharField(max_length=10)
    expense_name = models.CharField(max_length=255)
    expense_amount = models.CharField(max_length=255)
    expense_quantity = models.CharField(max_length=255)
    qty_unit = models.CharField(max_length=255)
    bill = models.ImageField(upload_to='users0_bill',default=None,null=True)
    extra_note = models.TextField()
    expense_date = models.CharField(max_length=255)