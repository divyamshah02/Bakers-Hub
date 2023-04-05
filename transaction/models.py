from django.db import models

# Create your models here.
class sales(models.Model):
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
    
class expense(models.Model):
    user_id = models.CharField(max_length=10)
    expense_name = models.CharField(max_length=255)
    expense_amount = models.CharField(max_length=255)
    expense_quantity = models.CharField(max_length=255)
    qty_unit = models.CharField(max_length=255)
    extra_note = models.TextField()
    expense_date = models.CharField(max_length=255)