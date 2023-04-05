from django.contrib import admin
from user_profile.models import UserProfile,Category

# Register your models here.
class AdminUserProfile(admin.ModelAdmin):
    list_display = ('email','user_id','pfp','otp','first_name','last_name')
    
admin.site.register(UserProfile,AdminUserProfile)

class AdminCategory(admin.ModelAdmin):
    list_display = ('user_id','category')
    
admin.site.register(Category,AdminCategory)