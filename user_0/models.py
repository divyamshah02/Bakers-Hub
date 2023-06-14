from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user_id = models.CharField(max_length=10)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    pfp = models.ImageField(upload_to='users0_pfp')
    theme_selection = models.CharField(default=0,max_length=2)
    otp = models.CharField(max_length=6)
    first_view = models.CharField(max_length=1,default=1)
    join_date = models.CharField(max_length=255,default=0)
    free_end_date = models.CharField(max_length=255,default=0)
    first_login = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)
    premium_start_date = models.CharField(max_length=255, default=0)
    premium_end_date = models.CharField(max_length=255, default=0)
    premium_month_plan = models.CharField(max_length=10,default=0)
    payment_id = models.CharField(max_length=255,default=0)
    
class Category(models.Model):
    user_id = models.CharField(max_length=10)
    category = models.CharField(max_length=255)
    
class Sale(models.Model):
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
    
class Ticket(models.Model):
    ticket_number = models.CharField(max_length=5)
    user_id = models.CharField(max_length=10)
    from_email = models.CharField(max_length=255)
    issue = models.TextField()
    date_time = models.CharField(max_length=255)
    subject = models.TextField()
    solved = models.BooleanField(default=False)
    