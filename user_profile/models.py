from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user_id = models.CharField(max_length=10)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    pfp = models.ImageField(upload_to='s_pfps')
    otp = models.CharField(max_length=6)
    
    
class Category(models.Model):
    user_id = models.CharField(max_length=10)
    category = models.CharField(max_length=255)